# external modules import
from pydantic import BaseModel, Field

# internal modules import
from modules import LicenseName, LicenseCode


# template definition
class License(BaseModel):
    """
    This class models a cooking license. Licenses may be referred to as abilities.
    """
    name: LicenseName = Field(title='License Name', description='Name of the cooking license.')
    code: LicenseCode = Field(title='License Code', description='Code of the cooking license.')
    level: int = Field(title='License Level', description='Level of the cooking license.')
