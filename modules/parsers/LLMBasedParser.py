# external modules import
import re
import time
import functools
from loguru import logger
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException

# internal modules import
from ..configs import LBPConfig
from ..templates import LicensesList, IngredientsList


# class definition
class LLMBasedParser:

    # constructor
    def __init__(self, config: LBPConfig):

        # initialize llm object
        self.model = OllamaLLM(model=config.ollama_model_name, base_url=config.ollama_server_uri)

    # decorators
    @staticmethod
    def retry_on_exception(max_retries, delay):
        max_retries_, delay_ = max_retries, delay

        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                attempts = 0
                while True:
                    try:
                        return func(self, *args, **kwargs)
                    except OutputParserException as e:
                        logger.info(f'Retrying {func.__name__} Execution')
                        attempts += 1
                        if attempts < max_retries_:
                            time.sleep(delay_)
                        else:
                            raise e

            return wrapper

        return decorator

    # public methods
    @retry_on_exception(max_retries=5, delay=1)
    def extract_chef_name(self, input_text: str) -> str:

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced document parser that extracts the fullname of a chef from a text written in italian.\n'
                'Return only the fullname.\n'
                'Text: {input_text}'
            ),
            input_variables=[
                'input_text'
            ]
        )

        # query llm
        llm_response = (prompt | self.model).invoke(
            {
                'input_text': input_text
            }
        )

        # response cleaning
        chef_name = re.sub(r'[\r\n]+', '', llm_response).strip()

        return chef_name

    @retry_on_exception(max_retries=5, delay=1)
    def extract_chef_licenses(self, input_text: str) -> LicensesList:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=LicensesList)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced document parser that extracts the licenses of a chef from a text written in italian.\n'
                'Extract the licenses from the given text and output in JSON format:\n'
                '{format_instructions}\n'
                'Make sure the output is fully compliant with the provided JSON schema. In particular:\n'
                '* ALWAYS specify all the attributes for every extracted license.\n'
                '* USE ONLY names and codes available in the schema, DO NOT invent them. If you find any name or code'
                'that is not in the schema, map it to the most plausible one in the schema.\n\n'
                'Text: {input_text}'
            ),
            input_variables=[
                'input_text'
            ],
            partial_variables={
                'format_instructions': parser.get_format_instructions()
            }
        )

        # query llm
        licenses_list = (prompt | self.model | parser).invoke(
            {
                'input_text': input_text
            }
        )

        return licenses_list

    @retry_on_exception(max_retries=5, delay=1)
    def extract_dish_ingredients(self, input_text: str) -> IngredientsList:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=IngredientsList)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced document parser that extracts information from a text written in italian.\n'
                'Extract the following fields from the given text and output in JSON format:\n'
                '{format_instructions}\n'
                'Make sure the output is fully compliant with the provided JSON schema, and do not skip mandatory fields.\n\n'
                'Text: {input_text}'
            ),
            input_variables=[
                'input_text'
            ],
            partial_variables={
                'format_instructions': parser.get_format_instructions()
            }
        )

        # query llm
        ingredients_list = (prompt | self.model | parser).invoke(
            {
                'input_text': input_text
            }
        )

        return ingredients_list
