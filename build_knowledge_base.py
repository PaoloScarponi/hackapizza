# external modules import
import os
from pathlib import Path
from dotenv import load_dotenv

# internal modules import
from modules import LBPConfig, LLMBasedParser, KBMConfig, KnowledgeBaseManager


# function definition
def build_knowledge_base(kb_manager: KnowledgeBaseManager, menus_path: Path) -> None:
    for menu_path in menus_path.glob('*pkl'):
        kb_manager.memorize_dishes(augmented_dishes=kb_manager.process_menu(menu_path=menu_path))
        menu_path.rename(menu_path.parent / 'done' / menu_path.name)

    return


# main-like execution
if __name__ == '__main__':

    # load/setup environment variables
    os.environ['HF_HOME'] = './ data / cache'
    load_dotenv()

    # create knowledge base manager object
    kb_manager_ = KnowledgeBaseManager(
        config=KBMConfig(
            manual_path=Path(__file__).parent / 'data' / 'raw' / 'Manuale di Cucina.pdf',
            code_path=Path(__file__).parent / 'data' / 'raw' / 'Codice Galattico.pdf',
            dishes_codes_path=Path(__file__).parent / 'data' / 'dish_mapping.json',
            kb_path=Path(__file__).parent / 'data' / 'processed' / 'dishes'
        ),
        llm_based_parser=LLMBasedParser(
            config=LBPConfig(
                ollama_server_uri=os.getenv('OLLAMA_SERVER_URI'),
                ollama_model_name=os.getenv('LBP_MODEL_NAME')
            )
        )
    )

    # execute knowledge base building pipeline
    build_knowledge_base(kb_manager=kb_manager_, menus_path=Path(__file__).parent / 'data' / 'processed' / 'menus')
