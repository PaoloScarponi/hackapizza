# external modules import
from typing import Dict, List, Tuple
from pydantic import BaseModel, Field

# internal modules import
from .Restaurant import Restaurant
from .IngredientsList import IngredientsList
from .TechniquesList import TechniquesList
from ..enums import Planet, LicenseName, LicenseCode


# template definition
class QMInfo(BaseModel):
    """
    This class models is meant to store the support information for the Query Manager.
    """
    planets_distances: Dict[Planet, Dict[Planet, int]] = Field(title='Planets Distances', description='A dictionary containing, for every planet, the distance from all others.')
    ingredients_list: IngredientsList = Field(title='Ingredients List', description='The list of all the known ingredients.')
    techniques_list: TechniquesList = Field(title='Techniques List', description='The list of all the known cooking techniques.')
    licenses_list: List[Tuple[LicenseName, LicenseCode]] = Field(title='Licenses List', description='The list of all the known cooking licenses name-code pairs.')
    restaurants_list: List[Restaurant] = Field(title='Techniques List', description='The list of all the known restaurants.')
