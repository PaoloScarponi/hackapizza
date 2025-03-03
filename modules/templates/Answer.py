# external modules import
from typing import List
from pydantic import BaseModel, Field


# template definition
class Answer(BaseModel):
    """
    This class models an answer representing a list of dishes that respect the constraints in the question.
    """
    dishes_codes: List[int] = Field(title='Dishes Codes', description='The list of codes representing the dishes.')
