# external modules import
from typing import List
from pydantic import BaseModel, Field

# internal modules import
from ..enums import Order, Planet
from .Restaurant import Restaurant
from .LicensesList import LicensesList
from .IngredientsList import IngredientsList
from .TechniquesList import TechniquesList


# template definition
class Question(BaseModel):
    """
    This class models a question that aims at finding dishes in the Knowledge Base based on some constraints.
    """
    desired_ingredients:  IngredientsList = Field(
        default=IngredientsList(items=[]),
        title='Desired Ingredients',
        description='A list of desired ingredients based on a question of the form "Quali piatti contengono <ingredienti>?" or variations'
    )
    disallowed_ingredients: IngredientsList = Field(
        default=IngredientsList(items=[]),
        title='Disallowed Ingredients',
        description='A list of disallowed ingredients based on a question of the form "Quali piatti NON contengono <ingredienti>?" or variations'
    )
    desired_techniques: TechniquesList = Field(
        default=TechniquesList(items=[]),
        title='Desired Techniques',
        description='A list of desired techniques based on a question of the form "Quali piatti sono preparati utilizzando <tecniche>?" or variations'
    )
    disallowed_techniques: TechniquesList = Field(
        default=TechniquesList(items=[]),
        title='Disallowed Techniques',
        description='A list of disallowed techniques based on a question of the form "Quali piatti NON sono preparati utilizzando <tecniche>?" or variations'
    )
    compatible_orders: List[Order] = Field(
        default=[],
        title='Compatible Orders',
        description='A list of compatible orders based on a question of the form "Quali piatti sono adatti per <ordini>?" or variations'
    )
    incompatible_orders: List[Order] = Field(
        default=[],
        title='Incompatible Orders',
        description='A list of incompatible orders based on a question of the form "Quali piatti NON sono adatti per <ordini>?" or variations'
    )
    chef_licenses: LicensesList = Field(
        default=LicensesList(items=[]),
        title='Chef Licenses',
        description='A list of licenses the chef should have based on a question of the form "Quali piatti sono preparati da chef con <licenze>??" or variations'
    )
    restaurants: List[Restaurant] = Field(
        default=[],
        title='Restaurants',
        description='A list of acceptable restaurants based on a question of the form "Quali piatti sono preparati in <ristoranti>?" or variations'
    )
    planets: List[Planet] = Field(
        default=[],
        title='Planets',
        description='A list of acceptable planets based on questions of the form "Quali piatti sono preparati su <pianeti>?" or "Quali piatti sono preparati entro <distanza> da <pianeti>?" or variations'
    )
