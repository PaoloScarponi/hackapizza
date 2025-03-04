# external modules import
import json
from typing import List, Dict
from Levenshtein import distance
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, RetryWithErrorOutputParser

# internal modules import
from ..enums import Planet
from ..configs import QAConfig
from ..templates import BaseQuestion, IngredientsList, TechniquesList, Restaurant


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
    def build_base_question_object(
            self,
            question: str,
            ingredients: IngredientsList,
            techniques: TechniquesList,
            planets_distances: Dict[Planet, Dict[Planet, int]]
    ) -> BaseQuestion:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=BaseQuestion)
        retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=self.model, max_retries=2)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced question parser and Named Entity Recognizer that, given a specific question '
                'written in italian, populates an object representing it.\n'
                'To populate the ingredients, map those in the question to those in the list below:\n'
                '{ingredients}\n'
                'If you need information about cooking techniques, you can find it in the JSON below:\n'
                '{techniques}\n'
                'If you need information about planets names and distances, you can find it in the JSON below:\n'
                '{planets_distances}\n'
                'Extract question info and output in JSON format:\n'
                '{format_instructions}\n'
                'Make sure the output is fully compliant with the provided JSON schema, and DO NOT include any '
                'attribute if it is not explicitly mentioned in the question.\n\n'
                'Question: {question}'
            ),
            input_variables=[
                'question',
                'ingredients',
                'techniques',
                'planets_distances'
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
                'planets_distances': json.dumps({k.value: {kk.value: vv for kk, vv in v.items()} for k, v in planets_distances.items()})
            }
        )
        llm_response = self.model.invoke(prompt)
        question_object = retry_parser.parse_with_prompt(llm_response, prompt)

        return question_object

    def find_restaurants(self, question: str, restaurants: List[Restaurant]) -> List[Restaurant]:
        return [r for r in restaurants if self._fuzzy_substring_match(r.name, question, max_distance=3)]
