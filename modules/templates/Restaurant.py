# external modules import
from pydantic import BaseModel, Field

# internal modules import
from ..enums import Planet


# template definition
class Restaurant(BaseModel):
    """
    This class models a restaurant.
    """

    name: str = Field(title='Restaurant Name', description='The name of the restaurant.')
    planet: Planet = Field(title='Planet Name', description='The name of the planet where the restaurant is.')
