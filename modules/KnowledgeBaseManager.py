# external modules import
import re
import json
import pickle
import pdfplumber
from pathlib import Path
from loguru import logger
from pdfplumber.pdf import PDF
from Levenshtein import distance
from typing import List, Tuple, Dict
from docling_core.types.doc.document import DoclingDocument, DocItem, DocItemLabel

# internal modules import
from .enums import Planet
from .configs import KBMConfig
from .parsers import RuleBasedParser, LLMBasedParser
from .templates import Info, Restaurant, Chef, Dish, AugmentedDish


# class definition
class KnowledgeBaseManager:
    """
    This class implements all the capabilities to populate the Knowledge Base.

    """

    # constructor
    def __init__(self, config: KBMConfig, llm_based_parser: LLMBasedParser):

        # initialize llm object and knowledge base path
        self.llm_based_parser = llm_based_parser
        self.kb_path = config.kb_path

        # load cooking manual content
        manual = self._load_document(config.manual_path)
        logger.info('The Cooking Manual has been loaded.')

        # load code of conduct content
        code = self._load_document(config.code_path)
        logger.info('The Galactic Code of Conduct has been loaded.')

        # initialize supporting info object
        self.info = Info(
            planets_names=[x.value for x in Planet],
            licenses_info=self._extract_licenses_info(manual),                  # not used at the moment
            techniques_info=self._extract_techniques_info(manual),
            techniques_reqs=self._extract_techniques_reqs(code),                # not used at the moment
            dishes_codes=self._load_dishes_codes(config.dishes_codes_path)
        )

        # free memory
        del code, manual

    # non-public methods
    @ staticmethod
    def _load_document(file_path: Path) -> PDF:
        return pdfplumber.open(file_path)

    @staticmethod
    def _extract_licenses_info(document: PDF) -> str:
        document_content = ''
        for page in document.pages:
            if page_content := page.extract_text():
                document_content += page_content
        output_text = document_content.split('Capitolo 1:')[1].split('Capitolo 2')[0]
        output_text = re.sub(r'[ \t]+', ' ', output_text)
        output_text = re.sub(r'\n{3,}', '\n\n', output_text).strip()

        return output_text

    @staticmethod
    def _extract_techniques_info(document: PDF) -> Dict[str, str]:
        extraction_flag, technique_category, techniques = False, None, {}
        for page in document.pages:
            lines = page.extract_text_lines()
            for line in lines:
                if 'Capitolo 3:' in line['text']:
                    extraction_flag = True
                if extraction_flag:
                    if line['chars'][3]['size'] > 20:
                        technique_category = line['text'].split(':')[1].strip()
                    if 12 < line['chars'][3]['size'] < 14:
                        techniques[line['text']] = technique_category

        return techniques

    @staticmethod
    def _extract_techniques_reqs(document: PDF) -> str:
        document_content = ''
        for page in document.pages:
            if page_content := page.extract_text():
                document_content += page_content
        output_text = document_content.split('4 Licenze e Tecniche di Preparazione')[1].split('5 Sanzioni e Pene')[0]
        output_text = re.sub(r'[ \t]+', ' ', output_text)
        output_text = re.sub(r'\n{3,}', '\n\n', output_text)
        output_text = re.sub(r'789/\d{5} \d+° Giorno del Ciclo Cosmico 789', "", output_text).strip()

        return output_text

    @staticmethod
    def _load_dishes_codes(file_path: Path) -> Dict:
        with open(file_path, 'r') as file:
            dishes_codes = json.load(file)

        return dishes_codes

    @staticmethod
    def _find_menu_keyword(menu: DoclingDocument) -> int:
        for i, t in enumerate(menu.texts):
            if t.label == DocItemLabel.SECTION_HEADER and 'menu' in t.text.lower():
                return i

        return -1

    @staticmethod
    def _extract_restaurant_info(restaurant_texts: List[DocItem]) -> List[str]:
        return [t.text for t in restaurant_texts]

    def _extract_dishes_info(self, dishes_texts: List[DocItem]) -> Tuple[List[List[str]], List[bool]]:
        current_dish_info, dishes_info = [], []
        ingredients_flag, techniques_flag, dishes_flags = False, False, []
        for t in dishes_texts:
            if any([distance(t.text.lower(), dish_name.lower()) < 2 for dish_name in self.info.dishes_codes.keys()]):
                if len(current_dish_info) > 0:
                    dishes_info.append(current_dish_info)
                    dishes_flags.append(all([ingredients_flag, techniques_flag]))
                    current_dish_info, ingredients_flag, techniques_flag = [], False, False
            if distance(t.text.lower(), 'ingredienti') <= 1:
                ingredients_flag = True
            if distance(t.text.lower(), 'tecniche') <= 1 or distance(t.text.lower(), 'techniques') <= 1:
                techniques_flag = True
            current_dish_info.append(t.text)
        dishes_info.append(current_dish_info)

        return dishes_info, dishes_flags

    @staticmethod
    def _populate_restaurant(restaurant_info: List[str]) -> Restaurant:
        restaurant_name = RuleBasedParser.extract_restaurant_name(
            input_text=restaurant_info
        )
        restaurant_planet = RuleBasedParser.extract_restaurant_planet(
            input_text=restaurant_info
        )

        return Restaurant(name=restaurant_name, planet=restaurant_planet)

    def _populate_chef(self, restaurant_info: List[str]) -> Chef:
        chef_name = self.llm_based_parser.extract_chef_name(
            input_text=(r_info_str := '\n'.join(restaurant_info))
        )
        chef_licenses = self.llm_based_parser.extract_chef_licenses(
            input_text=r_info_str
        )

        return Chef(name=chef_name, licenses=chef_licenses)

    def _populate_dish(self, dishes_info: List[str], dishes_flag: bool) -> Dish:
        # TODO: implement logic to handle orders.
        dish_code, dish_name = 0, ''
        for d_name, d_code in self.info.dishes_codes.items():
            if distance(dishes_info[0], d_name) <= 2:
                dish_code, dish_name = d_code, d_name
                break
        if dishes_flag:
            dish_ingredients = RuleBasedParser.extract_dish_ingredients(
                input_text=dishes_info
            )
            dish_techniques = RuleBasedParser.extract_dish_techniques_v1(
                input_text=dishes_info,
                additional_info=self.info.techniques_info
            )
        else:
            dish_ingredients = self.llm_based_parser.extract_dish_ingredients(
                input_text='\n'.join(dishes_info)
            )
            dish_techniques = RuleBasedParser.extract_dish_techniques_v2(
                input_text=dishes_info,
                additional_info=self.info.techniques_info
            )

        return Dish(code=dish_code, name=dish_name, ingredients=dish_ingredients, techniques=dish_techniques)

    # public methods
    def process_menu(self, menu_path: Path) -> List[AugmentedDish]:

        # initialize output
        augmented_dishes = []

        # load document
        with open(menu_path, 'rb') as f:
            menu: DoclingDocument = pickle.load(f)

        # extract dishes information
        menu_keyword_position = self._find_menu_keyword(menu=menu)
        if menu_keyword_position != -1:

            # preprocess document content
            restaurant_info = self._extract_restaurant_info(restaurant_texts=menu.texts[0:menu_keyword_position])
            dishes_info, dishes_flags = self._extract_dishes_info(dishes_texts=menu.texts[(menu_keyword_position + 1):])

            # extract restaurant
            restaurant = self._populate_restaurant(restaurant_info=restaurant_info)
            logger.info(f'Currently Processing {restaurant.name}')

            # extract chef info
            chef = self._populate_chef(restaurant_info=restaurant_info)
            logger.info(f' - Chef Extracted: {chef.name}')

            # extract ingredients and techniques for each dish
            for current_dish_info, current_dish_flag in zip(dishes_info, dishes_flags):
                augmented_dishes.append(
                    AugmentedDish(
                        restaurant=restaurant,
                        chef=chef,
                        dish=self._populate_dish(dishes_info=current_dish_info, dishes_flag=current_dish_flag)
                    )
                )
                logger.info(f' - Dish Extracted: {augmented_dishes[-1].dish.name}')

        return augmented_dishes

    def memorize_dishes(self, augmented_dishes: List[AugmentedDish]) -> None:
        for ad in augmented_dishes:
            with open(self.kb_path / (str(ad.dish.code) + '.json'), 'w') as f:
                f.write(ad.model_dump_json(indent=4))

        return
