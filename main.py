# external modules import
from dotenv import load_dotenv
from pathlib import Path
import os

# internal modules import
from modules import KBMConfig, KnowledgeBaseManager


# function definition
def main():
    pass


# main-like execution
if __name__ == '__main__':
    load_dotenv()
    kb_manager = KnowledgeBaseManager(
        config=KBMConfig(
            model_name=os.getenv('LLM_NAME'),
            model_uri=os.getenv('LLM_URI'),
            manual_path=Path(__file__).parent / 'data' / 'raw' / 'Manuale di Cucina.pdf',
            code_path=Path(__file__).parent / 'data' / 'raw' / 'Codice Galattico.pdf',
            dishes_codes_path=Path(__file__).parent / 'data' / 'dish_mapping.json',
        )
    )
