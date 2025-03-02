# external modules import
from pydantic import BaseModel, Field
from typing import Dict

# internal modules import
from .IngredientsList import IngredientsList
from .TechniquesList import TechniquesList


# template definition
class Dish(BaseModel):
    """
    This class models a dish.

    """

    code: int = Field(
        title='Dish Code',
        description='The code of the dish.'
    )
    name: str = Field(
        title='Dish Name',
        description='The name of the dish.'
    )
    ingredients: IngredientsList = Field(
        title='Ingredients List',
        description='The list of ingredients of the dish.'
    )
    techniques: TechniquesList = Field(
        title='Techniques List',
        description='The list of techniques used to cook the dish.'
    )
    andromeda_flag: bool = Field(
        title='Andromeda Order Flag',
        description='A boolean flag indicating if the dish can be eaten by people of the Andromeda Order.'
    )
    armonisti_flag: bool = Field(
        title='Armonisti Order Flag',
        description='A boolean flag indicating if the dish can be eaten by people of the Armonisti Order.'
    )
    naturalisti_flag: bool = Field(
        title='Naturalisti Order Flag',
        description='A boolean flag indicating if the dish can be eaten by people of the Naturalisti Order.'
    )
