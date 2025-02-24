# external modules import
from pydantic import BaseModel, Field

# internal modules import
from .LicensesList import LicensesList


# template definition
class Chef(BaseModel):
    """
    This class models a chef.
    """

    name: str = Field(title='Chef Name', description='The name of the chef.')
    licenses: LicensesList = Field(title='Licenses List', description='The list of cooking licenses of the chef.')
