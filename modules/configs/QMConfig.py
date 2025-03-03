# external modules import
from pathlib import Path
from dataclasses import dataclass


# class definition
@dataclass
class QMConfig:
    kb_path: Path
    planet_distances_path: Path
    questions_templates_path: Path
