# external modules import
import json
from typing import List, Dict
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

# internal modules import
from .enums import Planet
from .configs import QAConfig
from .templates import Answer, AugmentedDish


# class definition
class QueryAgent:

    # constructor
    def __init__(self, config: QAConfig):

        # initialize llm object
        self.model = OllamaLLM(model=config.ollama_model_name, base_url=config.ollama_server_uri, temperature=0.1)

    # public methods
    def answer_question(self, question: str, knowledge_base: List[AugmentedDish], planets_distances: Dict[Planet, Dict[Planet, int]]) -> Answer:

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
                'planet_distances'
            ],
            partial_variables={
                'format_instructions': parser.get_format_instructions()
            }
        )

        # query llm
        licenses_list = (prompt | self.model | parser).invoke(
            {
                'question': question,
                'knowledge_base': '\n'.join([d.model_dump_json(indent=2) for d in knowledge_base]),
                'planet_distances': json.dumps(planets_distances, indent=2)
            }
        )

        return licenses_list