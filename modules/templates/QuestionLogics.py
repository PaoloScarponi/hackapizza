# external modules import
from typing import List
from pydantic import BaseModel, Field


# internal modules import
from ..enums import LogicalOperator


# template definition
class QuestionLogics(BaseModel):
    """
    This class models the logical relationships between important entities in a question that aims at finding dishes in the Knowledge Base based on some constraints.
    """
    desired_ingredients_lo: LogicalOperator | None = Field(
        default=None,
        title='desired Ingredients Logical Operators',
        description='The logical operator that connects the allowed ingredients when converting the original question into a query on a generic database.'
    )
    desired_techniques_lo: LogicalOperator | None = Field(
        default=None,
        title='Desired Techniques Logical Operators',
        description='The logical operator that connects the allowed techniques when converting the original question into a query on a generic database.'
    )
    chef_licenses_lo: List[LogicalOperator] | None = Field(
        default=None,
        title='Desired Licenses Logical Operators',
        description='The logical operator that connects the allowed licenses when converting the original question into a query on a generic database.'
    )
