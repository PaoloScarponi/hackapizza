# external modules import
from typing import Dict
from pydantic import BaseModel, Field

# internal modules import
from ..enums import Planet
from .IngredientsList import IngredientsList
from .TechniquesList import TechniquesList


# template definition
class QMInfo(BaseModel):
    """
    This class models is meant to store the support information for the Query Manager.
    """

    questions_templates: Dict[str, int] = Field(title='Questions Templates', description='A dictionary containing the questions templates, each with a unique identifier.')
    planets_distances: Dict[Planet, Dict[Planet, int]] = Field(title='Planets Distances', description='A dictionary containing, for every planet, the distance from all others.')
    ingredients_list: IngredientsList = Field(title='Ingredients List', description='The list of all the known ingredients.')
    techniques_list: TechniquesList = Field(title='Techniques List', description='The list of all the known cooking techniques.')
