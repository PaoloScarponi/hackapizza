# external modules import
import csv
import copy
import json
from pathlib import Path
from loguru import logger
from Levenshtein import distance
from typing import List, Dict, Tuple

# internal modules import
from .configs import QMConfig
from .agents import QueryAgent
from .enums import Planet, LicenseName, LicenseCode, LogicalOperator
from .templates import QMInfo, AugmentedDish, Restaurant, License, Ingredient, IngredientsList, Technique, TechniquesList, Question, QuestionLogics, Answer


# class definition
class QueryManager:
    """
    This class implements all the capabilities to query the Knowledge Base.
    """

    # constructor
    def __init__(self, config: QMConfig, query_agent: QueryAgent):

        # initialize query agent object
        self.query_agent = query_agent

        # load knowledge base into memory
        self.knowledge_base = self._load_knowledge_base(config.kb_path)

        # initialize supporting info object
        self.info = QMInfo(
            planets_distances=self._load_planets_distances(config.planet_distances_path),
            ingredients_list=self._extract_ingredients_list(),
            techniques_list=self._extract_techniques_list(),
            licenses_list=self._load_licenses_list(),
            restaurants_list=self._extract_restaurants()
        )

    # non-public methods
    @staticmethod
    def _load_questions_templates(file_path: Path) -> Dict[str, int]:
        with open(file_path, 'r') as file:
            questions_templates = json.load(file)

        return questions_templates

    @staticmethod
    def _load_knowledge_base(file_path: Path) -> List[AugmentedDish]:
        knowledge_base = []
        for dish_path in file_path.glob('*.json'):
            with open(dish_path, 'r', encoding='utf-8') as file:
                knowledge_base.append(AugmentedDish(**json.load(file)))

        return knowledge_base

    @staticmethod
    def _load_planets_distances(file_path: Path) -> Dict[Planet, Dict[Planet, int]]:
        planets_distances = {}
        with open(file_path, 'r') as f:
            for line_number, line_content in enumerate(csv.reader(f, delimiter=',')):
                if line_number == 0:
                    distances_maps = [Planet(p) for p in line_content[1:]]
                    continue
                planets_distances[Planet(line_content[0])] = {Planet(p): int(d) for p, d in zip(distances_maps, line_content[1:])}

        return planets_distances

    def _extract_ingredients_list(self) -> IngredientsList:
        ingredients = []
        for ad in self.knowledge_base:
            ingredients.extend(ad.dish.ingredients.items)

        return IngredientsList(items=ingredients)

    def _extract_techniques_list(self) -> TechniquesList:
        techniques = []
        for ad in self.knowledge_base:
            techniques.extend(ad.dish.techniques.items)

        return TechniquesList(items=techniques)

    @staticmethod
    def _load_licenses_list() -> List[Tuple[LicenseName, LicenseCode]]:
        return [(l_name, l_code) for l_name, l_code in zip(LicenseName, LicenseCode)]

    def _extract_restaurants(self) -> List[Restaurant]:
        restaurants = []
        for ad in self.knowledge_base:
            if ad.restaurant not in restaurants:
                restaurants.append(ad.restaurant)

        return restaurants

    def _understand_question(self, question: str) -> Question:
        # TODO (Low): implement the logic to understand orders.
        base_question = self.query_agent.build_base_question_object(
            question=question,
            ingredients=self.info.ingredients_list,
            techniques=self.info.techniques_list,
            planets_distances = self.info.planets_distances
        )
        restaurants = self.query_agent.find_restaurants(
            question=question,
            restaurants=self.info.restaurants_list
        )
        if 'chef' in question.lower():
            licenses = self.query_agent.find_licenses(
                question=question,
                licenses=self.info.licenses_list
            ).items
        else:
            licenses = []

        return Question(**base_question.model_dump(), restaurants=restaurants, chef_licenses=licenses)

    def _understand_logical_operators(self, question: str, question_object: Question) -> QuestionLogics:
        return self.query_agent.understand_operators(question=question, question_object=question_object)

    @staticmethod
    def _filter_dishes_by_desired_ingredients(
            input_dishes: List[AugmentedDish],
            ingredients_list: List[Ingredient],
            logical_operator: LogicalOperator
    ) -> List[AugmentedDish]:
        if len(ingredients_list) == 0:
            return input_dishes
        if logical_operator == LogicalOperator.AND:
            output_dishes = copy.deepcopy(input_dishes)
            for ingredient in ingredients_list:
                output_dishes = [ad for ad in output_dishes if any(distance(i.name.lower(), ingredient.name.lower()) <= 2 for i in ad.dish.ingredients.items)]
        else:
            output_dishes = []
            for ingredient in ingredients_list:
                output_dishes.extend([ad for ad in input_dishes if any(distance(i.name.lower(), ingredient.name.lower()) <= 2 for i in ad.dish.ingredients.items)])

        return output_dishes

    @staticmethod
    def _filter_dishes_by_disallowed_ingredients(
            input_dishes: List[AugmentedDish],
            ingredients_list: List[Ingredient]
    ) -> List[AugmentedDish]:
        output_dishes = copy.deepcopy(input_dishes)
        for ingredient in ingredients_list:
            output_dishes = [ad for ad in output_dishes if not any(distance(i.name.lower(), ingredient.name.lower()) <= 2 for i in ad.dish.ingredients.items)]

        return output_dishes

    @staticmethod
    def _filter_dishes_by_desired_techniques(
            input_dishes: List[AugmentedDish],
            techniques_list: List[Technique],
            logical_operator: LogicalOperator
    ) -> List[AugmentedDish]:
        if len(techniques_list) == 0:
            return input_dishes
        if logical_operator == LogicalOperator.AND:
            output_dishes = copy.deepcopy(input_dishes)
            for technique in techniques_list:
                output_dishes = [ad for ad in output_dishes if any(distance(i.name.lower(), technique.name.lower()) <= 2 for i in ad.dish.techniques.items)]
        else:
            output_dishes = []
            for technique in techniques_list:
                output_dishes.extend([ad for ad in input_dishes if any(distance(i.name.lower(), technique.name.lower()) <= 2 for i in ad.dish.techniques.items)])

        return output_dishes

    @staticmethod
    def _filter_dishes_by_disallowed_techniques(
            input_dishes: List[AugmentedDish],
            techniques_list: List[Technique]
    ) -> List[AugmentedDish]:
        output_dishes = copy.deepcopy(input_dishes)
        for technique in techniques_list:
            output_dishes = [ad for ad in output_dishes if not any(distance(i.name, technique.name) <= 2 for i in ad.dish.techniques.items)]

        return output_dishes

    @staticmethod
    def _filter_dishes_by_planets(input_dishes: List[AugmentedDish], planets_list: List[Planet]) -> List[AugmentedDish]:
        if len(planets_list) == 0:
            return input_dishes
        output_dishes = []
        for planet in planets_list:
            output_dishes.extend([ad for ad in input_dishes if planet == ad.restaurant.planet])

        return output_dishes

    @staticmethod
    def _filter_dishes_by_restaurants(input_dishes: List[AugmentedDish], restaurants_list: List[Restaurant]) -> List[AugmentedDish]:
        if len(restaurants_list) == 0:
            return input_dishes
        output_dishes = []
        for restaurant in restaurants_list:
            output_dishes.extend([ad for ad in input_dishes if restaurant == ad.restaurant])

        return output_dishes

    @staticmethod
    def _filter_dishes_by_licenses(input_dishes: List[AugmentedDish], licenses_list: List[License]) -> List[AugmentedDish]:
        output_dishes = copy.deepcopy(input_dishes)
        for license_ in licenses_list:
            output_dishes = [ad for ad in input_dishes if any((i.code == license_.code and i.level >= license_.level) for i in ad.chef.licenses.items)]

        return output_dishes

    # public methods
    def answer_question(self, question: str) -> Answer:

        # understand subquestions types and parameters
        logger.info('Original Question: ' + question.strip('\n'))
        question_object = self._understand_question(question=question)
        logger.info('Parsed Question: ' + question_object.model_dump_json())

        # understand the relationships between subquestions
        if any(
                [
                    len(question_object.desired_ingredients) > 1,
                    len(question_object.desired_techniques) > 1,
                    len(question_object.chef_licenses) > 1,
                ]
        ):
            relationships_sequence = self._understand_logical_operators(question=question, question_object=question_object)
            logger.info(relationships_sequence)
        else:
            relationships_sequence = QuestionLogics()

        # execute sequence of queries based on subquestions relationships
        output_dishes = self._filter_dishes_by_desired_ingredients(
            input_dishes=self.knowledge_base,
            ingredients_list=question_object.desired_ingredients,
            logical_operator=relationships_sequence.desired_ingredients_lo
        )
        output_dishes = self._filter_dishes_by_disallowed_ingredients(
            input_dishes=output_dishes,
            ingredients_list=question_object.disallowed_ingredients
        )
        output_dishes = self._filter_dishes_by_desired_techniques(
            input_dishes=output_dishes,
            techniques_list=question_object.desired_techniques,
            logical_operator=relationships_sequence.desired_techniques_lo
        )
        output_dishes = self._filter_dishes_by_disallowed_techniques(
            input_dishes=output_dishes,
            techniques_list=question_object.disallowed_techniques
        )
        output_dishes = self._filter_dishes_by_planets(
            input_dishes=output_dishes,
            planets_list=question_object.planets
        )
        output_dishes = self._filter_dishes_by_restaurants(
            input_dishes=output_dishes,
            restaurants_list=question_object.restaurants
        )
        output_dishes = self._filter_dishes_by_licenses(
            input_dishes=output_dishes,
            licenses_list=question_object.chef_licenses
        )

        return Answer(dishes_codes=[x.dish.code for x in output_dishes])

    @staticmethod
    def memorize_answers(answers: Dict[int, Answer]) -> None:
        with open(Path(__file__).parent.parent / 'data' / 'test_answers.csv', 'w', encoding='utf-8', newline='') as f:
            f.write('row_id,result\n')
            for k, v in answers.items():
                f.write(','.join([str(k), f'\"{",".join([str(c) for c in v.dishes_codes])}\"']) + '\n')

        return

    # @staticmethod
    # def find_nearby_planets(
    #         planet: Planet,
    #         threshold: int,
    #         distance_matrix: Dict[Planet, Dict[Planet, int]]
    # ) -> List[Planet]:
    #     return [other_planet for other_planet, distance in distance_matrix[planet].items() if distance <= threshold]
