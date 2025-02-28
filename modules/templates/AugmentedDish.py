# external modules import
from pydantic import BaseModel, Field

# internal modules import
from .Restaurant import Restaurant
from .Chef import Chef
from .Dish import Dish


# template definition
class AugmentedDish(BaseModel):
    """
    This class models an augmented dish, that represents the basic entity in the Knowledge Base.

    """

    restaurant: Restaurant = Field(title='Dish Object', description='The object containing the information about the restaurant the dish is cooked in.')
    chef: Chef = Field(title='Chef Object', description='The object containing information about the chef cooking the dish.')
    dish: Dish = Field(title='Dish Object', description='The actual dish object.')
