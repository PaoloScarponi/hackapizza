# external modules import
from dataclasses import dataclass


# class definition
@dataclass
class QAConfig:
    ollama_server_uri: str
    ollama_model_name: str

