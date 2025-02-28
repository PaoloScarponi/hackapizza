# external modules import
from pydantic import BaseModel, Field

# internal modules import
from .IngredientsList import IngredientsList
from .TechniquesList import TechniquesList


# template definition
class Dish(BaseModel):
    """
    This class models a dish.

    """

    code: int = Field(title='Dish Code', description='The code of the dish.')
    name: str = Field(title='Dish Name', description='The name of the dish.')
    ingredients: IngredientsList = Field(title='Ingredients List', description='The list of ingredients of the dish.')
    techniques: TechniquesList = Field(title='Techniques List', description='The list of techniques used to cook the dish.')
