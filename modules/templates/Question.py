# external modules import
from typing import List
from pydantic import Field

# internal modules import
from .BaseQuestion import BaseQuestion
from .Restaurant import Restaurant
from .License import License


# template definition
class Question(BaseQuestion):
    """
    This class models an extended question that aims at finding dishes in the Knowledge Base based on some constraints.
    """
    restaurants: List[Restaurant] = Field(
        default=[],
        title='Restaurants',
        description='A list of acceptable restaurants based on a question of the form "Quali piatti sono preparati in <ristoranti>?" or variations'
    )
    chef_licenses: List[License] = Field(
        default=[],
        title='Chef Licenses',
        description='A list of licenses the chef should have based on a question of the form "Quali piatti sono preparati da chef con <licenze>??" or variations'
    )
    andromeda_flag: bool = Field(
        default=False,
        title='Andromeda Order Flag',
        description='A boolean flag indicating if the question asks about dishes that are suitable for people of the Andromeda Order.'
    )
    armonisti_flag: bool = Field(
        default=False,
        title='Armonisti Order Flag',
        description='A boolean flag indicating if the question asks about dishes that are suitable for people of the Armonisti Order.'
    )
    naturalisti_flag: bool = Field(
        default=False,
        title='Naturalisti Order Flag',
        description='A boolean flag indicating if the question asks about dishes that are suitable for people of the Naturalisti Order.'
    )
