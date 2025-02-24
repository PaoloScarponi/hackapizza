# external modules import
from pydantic import BaseModel, Field


# template definition
class License(BaseModel):
    """
    This class models a cooking license. Licenses may be referred to as abilities.
    """

    name: str = Field(title='License Name', description='Name of the cooking license.')
    code: str = Field(title='License Code', description='Code of the cooking license.')
    level: int = Field(title='License Level', description='Level of the cooking license.')
