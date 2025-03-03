# external modules import
from typing import List, Dict
from pydantic import BaseModel, Field

# internal modules import
from .Ingredient import Ingredient


# template definition
class IngredientsList(BaseModel):
    """
    This class models a list of ingredients.
    """
    items: List[Ingredient] = Field(title='Ingredients List', description='A list of ingredients.')
