# external modules import
import csv
import json
from pathlib import Path
from loguru import logger
from typing import List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

# internal modules import
from modules import Planet, AugmentedDish, Answer


# class definition
class PowerfulQueryAgent:

    # constructor
    def __init__(self):

        # initialize llm object
        self.model = ChatOpenAI(model='gpt-4o', temperature=0.1)

    # public methods
    @staticmethod
    def load_knowledge_base(file_path: Path) -> List[AugmentedDish]:
        knowledge_base = []
        for dish_path in file_path.glob('*.json'):
            with open(dish_path, 'r', encoding='utf-8') as file:
                knowledge_base.append(AugmentedDish(**json.load(file)))

        return knowledge_base

    @staticmethod
    def load_planets_distances(file_path: Path) -> Dict[Planet, Dict[Planet, int]]:
        planets_distances = {}
        with open(file_path, 'r') as f:
            for line_number, line_content in enumerate(csv.reader(f, delimiter=',')):
                if line_number == 0:
                    distances_maps = [Planet(p) for p in line_content[1:]]
                    continue
                planets_distances[Planet(line_content[0])] = {Planet(p): int(d) for p, d in zip(distances_maps, line_content[1:])}

        return planets_distances

    @staticmethod
    def memorize_answers(answers: Dict[int, Answer]) -> None:
        with open(Path(__file__).parent.parent / 'data' / 'test_answers.csv', 'w', encoding='utf-8', newline='') as f:
            f.write('row_id,result\n')
            for k, v in answers.items():
                f.write(','.join([str(k), f'\"{",".join([str(c) for c in v.dishes_codes])}\"']) + '\n')

        return

    def answer_question(
            self,
            question: str,
            knowledge_base: List[AugmentedDish],
            planets_distances: Dict[Planet, Dict[Planet, int]]
    ) -> Answer:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=Answer)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced question answering engine that provides the user with a list of dishes based on '
                'the constraints provided in their question.\n'
                'The question is in italian, and you have to answer by providing the codes of the dishes, which you can'
                'find in the list of JSONs below:\n'
                '{knowledge_base}\n'
                'If you need information about planets distances, you can find it in the JSON below:\n'
                '{planets_distances}'
                'Extract dishes codes and output in JSON format:\n'
                '{format_instructions}\n\n'
                'Question: {question}'
            ),
            input_variables=[
                'question',
                'knowledge_base',
                'planets_distances'
            ],
            partial_variables={
                'format_instructions': parser.get_format_instructions()
            }
        )

        # query llm
        licenses_list = (prompt | self.model | parser).invoke(
            {
                'question': question,
                'knowledge_base': '\n'.join([d.model_dump_json() for d in knowledge_base]),
                'planets_distances': json.dumps({k.value: {kk.value: vv for kk, vv in v.items()} for k, v in planets_distances.items()})
            }
        )

        return licenses_list

if __name__ == '__main__':
    load_dotenv()
    answers = {}
    powerful_agent = PowerfulQueryAgent()
    knowledge_base_ = powerful_agent.load_knowledge_base(Path(__file__).parent.parent / 'data' / 'processed' / 'dishes')
    planets_distances_ = powerful_agent.load_planets_distances(Path(__file__).parent.parent / 'data' / 'planets_distances.csv')
    with open(Path(__file__).parent / 'data' / 'test_questions.csv', 'r', encoding='utf-8') as f:
        for question_number, question_ in enumerate(f, start=1):
            answers_1 = powerful_agent.answer_question(
                question=question_,
                knowledge_base=knowledge_base_[0:100],
                planets_distances=planets_distances_
            )
            answers_2 = powerful_agent.answer_question(
                question=question_,
                knowledge_base=knowledge_base_[100:200],
                planets_distances=planets_distances_
            )
            answers_3 = powerful_agent.answer_question(
                question=question_,
                knowledge_base=knowledge_base_[200:],
                planets_distances=planets_distances_
            )
            answers[question_number] = Answer(dishes_codes=(answers_1.dishes_codes + answers_2.dishes_codes + answers_3.dishes_codes))
            logger.info(f'Question: {question_}')
            logger.info(f'Answer: {answers[question_number].dishes_codes}')
            if len(answers[question_number].dishes_codes) == 0:
                logger.warning('No Dish Found, Setting 0 as Default!')
                answers[question_number].dishes_codes.append(0)
    powerful_agent.memorize_answers(answers=answers)
