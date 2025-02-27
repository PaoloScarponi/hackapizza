# external modules import
import pickle
from pathlib import Path
from loguru import logger
from docling.document_converter import DocumentConverter


# function definition
def preprocess_menu(input_menus_path: Path, output_menus_path: Path) -> None:
    for menu_path in input_menus_path.glob('*pdf'):
        menu = DocumentConverter().convert(menu_path).document
        with open(output_menus_path / (menu_path.name[:-4] + '.pkl'), 'wb') as f:
            pickle.dump(menu, f)
        logger.info(f'{menu_path.name[:-4]} Menu Converted')

    return


# main-like execution
if __name__ == '__main__':
    preprocess_menu(
        input_menus_path=Path(__file__).parent / 'data' / 'raw' / 'menus',
        output_menus_path=Path(__file__).parent / 'data' / 'processed' / 'menus'
    )
