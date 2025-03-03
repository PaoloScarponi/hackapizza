# external modules import
import csv
import json
from pathlib import Path
from typing import List, Dict

# internal modules import
from .enums import Planet
from .configs import QMConfig
from .QueryAgent import QueryAgent
from .templates import QMInfo, AugmentedDish, Restaurant, License, Ingredient, IngredientsList, Technique, TechniquesList, Answer


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
            questions_templates=self._load_questions_templates(config.questions_templates_path),
            planets_distances=self._load_planets_distances(config.planet_distances_path),
            ingredients_list=self._extract_ingredients_list(),
            techniques_list=self._extract_techniques_list()
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
    def _filter_dishes_by_restaurant(input_dishes: List[AugmentedDish], restaurant: Restaurant) -> List[AugmentedDish]:
        return [ad for ad in input_dishes if restaurant.name == ad.restaurant.name]

    @staticmethod
    def _filter_dishes_by_planet(input_dishes: List[AugmentedDish], planet: Planet) -> List[AugmentedDish]:
        return [ad for ad in input_dishes if planet == ad.restaurant.planet]

    @staticmethod
    def _filter_dishes_by_chef_license(input_dishes: List[AugmentedDish], chef_license: License) -> List[AugmentedDish]:
        return [ad for ad in input_dishes if any(i == chef_license for i in ad.chef.licenses.items)]

    @staticmethod
    def _filter_dishes_by_ingredient(input_dishes: List[AugmentedDish], ingredient: Ingredient, exclude_flag: bool) -> List[AugmentedDish]:
        if not exclude_flag:
            output_dishes = [ad for ad in input_dishes if any(i == ingredient for i in ad.dish.ingredients.items)]
        else:
            output_dishes = [ad for ad in input_dishes if not any(i == ingredient for i in ad.dish.ingredients.items)]

        return output_dishes

    @staticmethod
    def _filter_dishes_by_technique(input_dishes: List[AugmentedDish], technique: Technique, exclude_flag: bool) -> List[AugmentedDish]:
        if not exclude_flag:
            output_dishes = [ad for ad in input_dishes if any(i == technique for i in ad.dish.techniques.items)]
        else:
            output_dishes = [ad for ad in input_dishes if not any(i == technique for i in ad.dish.techniques.items)]

        return output_dishes

    # public methods
    def answer_question(self, question: str) -> Answer:
        # 1. Understand subquestions types.
        # 2. Understand the relationships between subquestions (AND/OR).
        # 3. Extract parameters for each subquestion.
        # 4. Execute query for each subquestion.
        # 5. Combine results based on subquestions relationships.

        return self.query_agent.answer_question(
            question=question,
            knowledge_base=self.knowledge_base,
            planets_distances=self.info.planets_distances
        )

    @staticmethod
    def memorize_answers(answers: Dict[int, Answer]) -> None:
        with open(Path(__file__).parent.parent / 'data' / 'test_answers.json', 'w', encoding='utf-8') as f:
            json.dump({k: v.dishes_codes for k, v in answers}, f, indent=4)

        return
