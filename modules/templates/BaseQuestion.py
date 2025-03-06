# external modules import
from typing import List
from pydantic import BaseModel, Field

# internal modules import
from .Ingredient import Ingredient
from .Technique import Technique


# template definition
class BaseQuestion(BaseModel):
    """
    This class models a question that aims at finding dishes in the Knowledge Base based on some constraints.
    """
    desired_ingredients: List[Ingredient] = Field(
        default=[],
        title='Desired Ingredients',
        description='A list of desired ingredients based on a question of the form "Quali piatti contengono <ingredienti>?" or variations.'
    )
    disallowed_ingredients: List[Ingredient] = Field(
        default=[],
        title='Disallowed Ingredients',
        description='A list of disallowed ingredients based on a question of the form "Quali piatti NON contengono <ingredienti>?" or variations.'
    )
    desired_techniques: List[Technique] = Field(
        default=[],
        title='Desired Techniques',
        description='A list of desired techniques based on a question of the form "Quali piatti sono preparati utilizzando <tecniche>?" or variations.'
    )
    disallowed_techniques: List[Technique] = Field(
        default=[],
        title='Disallowed Techniques',
        description='A list of disallowed techniques based on a question of the form "Quali piatti NON sono preparati utilizzando <tecniche>?" or variations.'
    )
