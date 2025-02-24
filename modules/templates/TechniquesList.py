# external modules import
from typing import List
from pydantic import BaseModel, Field

# internal modules import
from .Technique import Technique


# template definition
class TechniqueList(BaseModel):
    """
    This class models a list of cooking techniques.
    """

    items: List[Technique] = Field(title='Techniques List', description='A list of cooking techniques.')
