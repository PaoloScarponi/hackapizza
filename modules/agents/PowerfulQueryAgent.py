# external modules import
import json
from typing import List, Dict
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

# internal modules import
from ..enums import Planet
from ..templates import AugmentedDish, Answer


# class definition
class PowerfulQueryAgent:

    def answer_question(
            self,
            question: str,
            knowledge_base: List[AugmentedDish],
            planets_distances: Dict[Planet,
            Dict[Planet, int]]
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
                'knowledge_base': '\n'.join([d.model_dump_json(indent=2) for d in knowledge_base]),
                'planets_distances': json.dumps(
                    {k.value: {kk.value: vv for kk, vv in v.items()} for k, v in planets_distances.items()}, indent=2)
            }
        )

        return licenses_list