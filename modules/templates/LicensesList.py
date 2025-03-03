# external modules import
from typing import List
from pydantic import BaseModel, Field

# internal modules import
from .License import License


# template definition
class LicensesList(BaseModel):
    """
    This class models a list of cooking licences.
    """
    items: List[License] = Field(title='Licenses List', description='A list of licenses.')
