# external modules import
from pydantic import BaseModel, Field

# internal modules import
from ..enums import IngredientCategory


# template definition
class Ingredient(BaseModel):
    """
    This class models an ingredient. Ingredients may be referred to as substances.
    """

    name: str = Field(title='Ingredient Name', description='Name of the ingredient.')
    # category: IngredientCategory = Field(title='Ingredient Category', description='Category of the ingredient.')
