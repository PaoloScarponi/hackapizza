# external modules import
from pathlib import Path
from dataclasses import dataclass


# class definition
@dataclass
class KBMConfig:
    manual_path: Path
    code_path: Path
    dishes_codes_path: Path
    kb_path: Path
