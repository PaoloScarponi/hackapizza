# external modules import
import re
import json
import pickle
import pdfplumber
from pathlib import Path
from loguru import logger
from typing import List, Dict
from Levenshtein import distance
from docling_core.types.doc.document import DoclingDocument, DocItem, DocItemLabel

# internal modules import
from .enums import Planet
from .configs import KBMConfig
from .LLMWrapper import LLMWrapper
from .templates import Info, Dish, Restaurant, Chef


# class definition
class KnowledgeBaseManager:

    # constructor
    def __init__(self, config: KBMConfig, llm_wrapper: LLMWrapper):
        """
        This is the constructor for a generic Knowledge Base Manager object.

        Parameters
        ----------
        config: KBMConfig
            The object containing all the parameters to set up a specific object of this class.

        """

        # initialize llm object
        self.llm_wrapper = llm_wrapper

        # extract cooking manual content
        manual_content = self._extract_document_content(config.manual_path)
        logger.info('The information from the Cooking Manual has been loaded.')

        # extract code of conduct content
        code_content = self._extract_document_content(config.code_path)
        logger.info('The Galactic Code of Conduct has been loaded.')

        # initialize supporting info object
        self.info = Info(
            planets_names=[x.value for x in Planet],
            licenses_info=self._extract_licenses_info(manual_content),
            techniques_info=self._extract_techniques_info(manual_content),
            techniques_reqs=self._extract_techniques_reqs(code_content),
            dishes_codes=self._load_dishes_codes(config.dishes_codes_path)
        )

    # non-public methods
    @ staticmethod
    def _extract_document_content(file_path: Path) -> str:
        file_content = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page_content := page.extract_text():
                    file_content += page_content

        return file_content

    @staticmethod
    def _extract_licenses_info(input_text: str) -> str:
        output_text = input_text.split('Capitolo 1:')[1].split('Capitolo 2')[0]
        output_text = re.sub(r'[ \t]+', ' ', output_text)
        output_text = re.sub(r'\n{3,}', '\n\n', output_text).strip()

        return output_text

    @staticmethod
    def _extract_techniques_info(input_text: str) -> str:
        output_text = input_text.split('Capitolo 3:')[1]
        output_text = re.sub(r"[^a-zA-ZàèéìòóùÀÈÉÌÒÓÙ0-9.,;:!?()'\"\s]", '', output_text)
        output_text = re.sub(r"([!?.,;:\-'])\1{2,}", r'\1\1', output_text)
        output_text = re.sub(r'\b[^\w\s]{3,}\b', '', output_text)
        output_text = re.sub(r'[ \t]+', ' ', output_text)
        output_text = re.sub(r'\n{3,}', '\n\n', output_text).strip()

        return output_text

    @staticmethod
    def _extract_techniques_reqs(input_text: str) -> str:
        output_text = input_text.split('4 Licenze e Tecniche di Preparazione')[1].split('5 Sanzioni e Pene')[0]
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

    def _extract_dishes_info(self, dishes_texts: List[DocItem]) -> List[List[str]]:
        dishes_info, current_dish_info = [], []
        for t in dishes_texts:
            if any([distance(t.text.lower(), dish_name.lower()) < 2 for dish_name in self.info.dishes_codes.keys()]):
                if len(current_dish_info) > 0:
                    dishes_info.append(current_dish_info)
                    current_dish_info = []
            current_dish_info.append(t.text)
        dishes_info.append(current_dish_info)

        return dishes_info

    @staticmethod
    def _populate_restaurant(restaurant_info: List[str]) -> Restaurant:
        restaurant_name = re.sub(r'Ristorante:|Ristorante "|"', '', restaurant_info[0]).strip()
        restaurant_planet = Planet.UNDISCLOSED
        r_info = '\n'.join(restaurant_info).lower()
        for p in Planet:
            if p.value.lower() in r_info:
                restaurant_planet = p
                break

        return Restaurant(name=restaurant_name, planet=restaurant_planet)

    def _populate_chef(self, restaurant_info: List[str]) -> Chef:
        chef_name = self.llm_wrapper.extract_chef_name(input_text='\n'.join(restaurant_info))
        chef_licenses = self.llm_wrapper.extract_chef_licenses(input_text='\n'.join(restaurant_info), additional_info=self.info.licenses_info)

        return Chef(name=chef_name, licenses=chef_licenses)

    # public methods
    def process_menu(self, menu_path: Path) -> List[Dish]:

        # initialize output
        dishes = []

        # load document
        with open(menu_path, 'rb') as f:
            menu: DoclingDocument = pickle.load(f)

        # extract dishes information
        menu_keyword_position = self._find_menu_keyword(menu=menu)
        if menu_keyword_position != -1:

            # preprocess document content
            restaurant_info = self._extract_restaurant_info(restaurant_texts=menu.texts[0:menu_keyword_position])
            dishes_info = self._extract_dishes_info(dishes_texts=menu.texts[(menu_keyword_position + 1):])

            # extract restaurant and chef info
            restaurant = self._populate_restaurant(restaurant_info=restaurant_info)
            chef = self._populate_chef(restaurant_info=restaurant_info)

            # extract ingredients and techniques for each dish
            # TODO: create a Dish object from each element in the dishes_info list

        return dishes
