# external modules import
from dataclasses import dataclass


# class definition
@dataclass
class LLMConfig:
    model_uri: str
    model_name: str
