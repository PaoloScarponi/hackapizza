# external modules import
from pathlib import Path
from dataclasses import dataclass


# class definition
@dataclass()
class KBMConfig:
    model_name: str
    model_uri: str
    manual_path: Path
    code_path: Path
    planets_names_path: Path
    dishes_codes_path: Path
