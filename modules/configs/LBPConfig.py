# external modules import
from dataclasses import dataclass


# class definition
@dataclass
class LBPConfig:
    ollama_server_uri: str
    ollama_model_name: str
