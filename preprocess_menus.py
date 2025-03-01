# external modules import
import pickle
import pdfplumber
from pathlib import Path
from loguru import logger
from docling.document_converter import DocumentConverter
from docling_core.types.doc.document import DoclingDocument, TextItem, DocItemLabel


# helper function
def create_docling_document(input_pdf_path) -> DoclingDocument:
    with pdfplumber.open(input_pdf_path) as pdf:
        doc = DoclingDocument(name=input_pdf_path.name)
        for page_number, page in enumerate(pdf.pages):
            lines = page.extract_text_lines()
            for line in lines:
                text_item = TextItem(text=line['text'], self_ref=f'#/texts/{page_number}', label=DocItemLabel.TEXT, prov=[], orig='')
                doc.texts.append(text_item)

    return doc

# main function definition
def preprocess_menu(input_menus_path: Path, output_menus_path: Path) -> None:
    for menu_path in input_menus_path.glob('*pdf'):
        if menu_path.name.split('.')[0] in ['Datapizza', 'L Essenza delle Dune', 'Le Dimensioni del Gusto']:
            # TODO: make this check adaptive
            menu = create_docling_document(menu_path)
        else:
            continue
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
