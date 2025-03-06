# external modules import
import re
import json
from Levenshtein import distance
from typing import List, Dict, Tuple
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain.output_parsers import PydanticOutputParser, RetryWithErrorOutputParser

# internal modules import
from ..configs import QAConfig
from ..enums import Planet, LicenseName, LicenseCode, Order
from ..templates import QuestionLogics, Question, BaseQuestion, IngredientsList, TechniquesList, Restaurant, LicensesList


# class definition
class QueryAgent:

    # constructor
    def __init__(self, config: QAConfig):

        # initialize llm object
        self.model = OllamaLLM(model=config.ollama_model_name, base_url=config.ollama_server_uri, temperature=0.1)

    # non-public methods
    @staticmethod
    def _fuzzy_substring_match(substring: str, text: str, max_distance: int) -> bool:
        sub_len = len(substring)
        for i in range(len(text) - sub_len + 1):
            if distance(substring, text[i:i + sub_len]) <= max_distance:
                return True

        return False

    # public methods
    def build_base_question_object(self, question: str, ingredients: IngredientsList, techniques: TechniquesList) -> BaseQuestion:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=BaseQuestion)
        retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=self.model, max_retries=6)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced Italian question parser and Named Entity Recognizer. Your task is to extract '
                'structured information from a given question and populate a JSON object.\n'
                'In doing so, keep the following guidelines in mind:\n'
                '* Identify ingredients mentioned in the question and map them to those in the provided list:\n'
                '{ingredients}\n'
                '* Identify cooking techniques and map them to those in the provided list:\n'
                '{techniques}\n'
                '* For specific techniques, focus on the name of each technique.\n'
                '* For open questions about a category of techniques, focus on the categories.\n'
                '* Ensure every ingredient and technique matches those from the provided lists, otherwise, omit them.\n'
                '* Infer techniques only when general subcategories are mentioned in the question.\n'
                '* Do NOT infer additional ingredients that are not explicitly mentioned.\n'
                '* If an ingredient contains multiple words, treat it as a single entity unless it matches a known technique.\n'
                'Extract question info and output in JSON format:\n'
                '{format_instructions}\n'
                'Make sure the output is fully compliant with the provided JSON schema.\n\n'
                'Question: {question}'
            ),
            input_variables=[
                'question',
                'ingredients',
                'techniques',
            ],
            partial_variables={
                'format_instructions': parser.get_format_instructions()
            }
        )

        # query llm
        prompt = prompt.invoke(
            {
                'question': question,
                'ingredients': ingredients.model_dump_json(),
                'techniques': techniques.model_dump_json(),
            }
        )
        llm_response = self.model.invoke(prompt)
        question_object = retry_parser.parse_with_prompt(llm_response, prompt)

        return question_object

    def find_restaurants(self, question: str, restaurants: List[Restaurant]) -> List[Restaurant]:
        return [r for r in restaurants if self._fuzzy_substring_match(r.name.lower(), question.lower(), max_distance=3)]

    @staticmethod
    def find_planets(question: str, planets_distances:  Dict[Planet, Dict[Planet, int]]) -> List[Planet]:
        # TODO (Low): Make this method more robust (planet name extraction, distance extraction and type casting).
        target_planet = None
        question_words = [w.strip('').strip(',').strip('.').lower() for w in question.split(' ')]
        for p in planets_distances.keys():
            if p.value.lower() in question_words:
                target_planet = p
                break
        if not target_planet:
            return []
        if 'anni luce' in question:
            threshold = int(question.split('anni luce')[0].strip().split(' ')[-1])
        else:
            threshold = 0
        planets_list = [planet for planet, distance_ in planets_distances[target_planet].items() if distance_ <= threshold]

        return planets_list

    def find_licenses(self, question: str, licenses: List[Tuple[LicenseName, LicenseCode]]) -> LicensesList:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=LicensesList)
        retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=self.model, max_retries=3)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced Named Entity Recognizer that, given a specific question written in italian, '
                'extract cooking licenses contained in it.\n'
                'The existing cooking licenses are provided in the JSON below:\n'
                '{licenses}\n'
                'Extract the relevant information from the question and output it in JSON format as the schema provided:\n'
                '{format_instructions}\n'
                'Make sure the output is fully compliant with the provided JSON schema.\n\n'
                'Question: {question}'
            ),
            input_variables=[
                'question',
                'licenses',
            ],
            partial_variables={
                'format_instructions': parser.get_format_instructions()
            }
        )

        # query llm
        prompt = prompt.invoke(
            {
                'question': question,
                'licenses': json.dumps({l[0].value: l[1].value for l in licenses})
            }
        )
        llm_response = self.model.invoke(prompt)
        try:
            licenses_list = retry_parser.parse_with_prompt(llm_response, prompt)
        except OutputParserException:
            licenses_list = LicensesList(items=[])

        return licenses_list

    @staticmethod
    def find_orders(question: str) -> Dict[str, bool]:
        question_words = [re.sub(r"[^a-zA-Z0-9\s]", "", w).strip('\n').strip().lower() for w in question.split(' ')]
        return {
            'andromeda_flag': Order.ANDROMEDA.name.lower() in question_words,
            'armonisti_flag': Order.ARMONISTI.name.lower() in question_words,
            'naturalisti_flag': Order.NATURALISTI.name.lower() in question_words
        }

    def understand_operators(self, question: str, question_object: Question) -> QuestionLogics:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=QuestionLogics)
        retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=self.model, max_retries=6)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced question parser that, given a specific question and a JSON descriptor that captures the'
                'main entities in the question, produces a sequence of logical operators to use for translating the question'
                'into a query of a generic database. Remember that "o" corresponds to "or" and "e" corresponds to "and".\n'
                '* Original Question: {question}\n'
                '* Question Descriptor: {question_object}\n'
                'Extract operators info and output in JSON format:\n'
                '{format_instructions}\n'
                'Make sure the output is fully compliant with the provided JSON schema.\n'
                'Examples:\n'
                '* INPUT: piatto con sale e pepe, OUTPUT: {{"desired_ingredients_lo": "and"}}\n'
                '* INPUT: piatto con sale o pepe, OUTPUT: {{"desired_ingredients_lo": "or"}}\n'
                '* INPUT: piatto con marinatura e bruciatura, OUTPUT: {{"desired_techniques_lo: "and"}}\n'
                '* INPUT: piatto con marinatura o bruciatura, OUTPUT: {{"desired_techniques_lo: "or"}}\n'
            ),
            input_variables=[
                'question',
                'question_object'
            ],
            partial_variables={
                'format_instructions': parser.get_format_instructions()
            }
        )

        # query llm
        prompt = prompt.invoke(
            {
                'question': question,
                'question_object': question_object.model_dump_json(),
            }
        )
        llm_response = self.model.invoke(prompt)
        question_object = retry_parser.parse_with_prompt(llm_response, prompt)

        return question_object
