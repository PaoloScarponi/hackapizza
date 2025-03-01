# external modules import
from typing import List, Dict
from pydantic import BaseModel, Field


# template definition
class Info(BaseModel):
    """
    This class models the information that are contained in the cooking manual and the galactic code of conduct.
    """

    planets_names: List[str] = Field(title='Planet Names', description='A list of all the available planets.')
    licenses_info: str = Field(title='Licenses Info', description='A string containing the info about cooking licenses.')
    techniques_info: dict = Field(title='Techniques Info', description='A dictionary containing the info about cooking techniques.')
    techniques_reqs: str = Field(title='Techniques Requirements', description='A string containing the requirements in term of abilities for any given technique.')
    dishes_codes: Dict = Field(title='Dishes Codes', description='A dictionary containing the mapping between dish names and codes.')
