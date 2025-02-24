# external modules import
from pydantic import BaseModel, Field


# template definition
class Dish(BaseModel):
    """
    This class models a dish.

    # TODO: update this model
    """

    code: int = Field(title='Dish Code', description='The code of the dish.')
    name: str = Field(title='Dish Name', description='The name of the dish.')
