# external modules import
from pydantic import BaseModel, Field

# internal modules import
from ..enums import TechniqueCategory, TechniqueSubcategory


# template definition
class Technique(BaseModel):
    """
    This class models a cooking technique.
    """
    name: str = Field(title='Technique Name', description='Name of the cooking technique.')
    category: TechniqueCategory = Field(title='Technique Category', description='Category of the cooking technique.')
    subcategory: TechniqueSubcategory = Field(title='Technique Sub-Category', description='Subcategory of the cooking technique.')
