# external modules import
from dotenv import load_dotenv
from pathlib import Path
import os

# internal modules import
from modules import KBMConfig, KnowledgeBaseManager


# function definition
def build_knowledge_base(kb_manager: KnowledgeBaseManager, menus_path: Path) -> None:

    dishes = []
    for menu_path in menus_path.glob('*pkl'):
        dishes.extend(kb_manager.process_menu(menu_path=menu_path))

    return


# main-like execution
if __name__ == '__main__':

    # load environment variables
    load_dotenv()

    # create knowledge base manager object
    kb_manager_ = KnowledgeBaseManager(
        config=KBMConfig(
            model_name=os.getenv('LLM_NAME'),
            model_uri=os.getenv('LLM_URI'),
            manual_path=Path(__file__).parent / 'data' / 'raw' / 'Manuale di Cucina.pdf',
            code_path=Path(__file__).parent / 'data' / 'raw' / 'Codice Galattico.pdf',
            planets_names_path=Path(__file__).parent / 'data' / 'planets_distances.csv',
            dishes_codes_path=Path(__file__).parent / 'data' / 'dish_mapping.json'
        )
    )

    # execute knowledge base building pipeline
    build_knowledge_base(kb_manager=kb_manager_, menus_path=Path(__file__).parent / 'data' / 'processed' / 'menus')
