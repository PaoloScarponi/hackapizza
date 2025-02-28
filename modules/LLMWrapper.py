# external modules import
import re
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

# internal modules import
from .configs import LLMConfig
from .templates import LicensesList, IngredientsList, TechniquesList


# class definition
class LLMWrapper:

    # constructor
    def __init__(self, config: LLMConfig):

        # initialize llm object
        self.model = OllamaLLM(model=config.model_name, base_url=config.model_uri)

    # public methods
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

    def extract_chef_licenses(self, input_text: str, additional_info: str) -> LicensesList:

        # initialize output parser
        parser = PydanticOutputParser(pydantic_object=LicensesList)

        # build prompt
        prompt = PromptTemplate(
            template=(
                'You are an advanced document parser that extracts information from a text written in italian.\n'
                'Extract the following fields from the given text and output in JSON format:\n'
                '{format_instructions}\n'
                'To understand the available licenses names and codes use the following additional info:\n'
                'Additional Info: {additional_info}\n'
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
        licenses_list = (prompt | self.model | parser).invoke(
            {
                'additional_info': additional_info,
                'input_text': input_text
            }
        )

        return licenses_list

    def extract_dish_ingredients(self, input_text: str) -> IngredientsList:
        pass

    def extract_dish_techniques(self, input_text: str, additional_info: str) -> TechniquesList:
        pass
