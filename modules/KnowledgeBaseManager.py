# external modules import
import re
import json
import pdfplumber
from pathlib import Path
from loguru import logger
from typing import List, Dict
from langchain_ollama.llms import OllamaLLM

# internal modules import
from .configs import KBMConfig
from .templates import Info, Dish


# class definition
class KnowledgeBaseManager:

    # constructor
    def __init__(self, config: KBMConfig):
        """
        This is the constructor for a generic Knowledge Base Manager object.

        Parameters
        ----------
        config: KBMConfig
            The object containing all the parameters to set up a specific object of this class.

        """

        # initialize llm object
        self.model = OllamaLLM(model=config.model_name, base_url=config.model_uri)

        # extract cooking manual content
        manual_content = self._extract_document_content(config.manual_path)
        logger.info('The information from the Cooking Manual has been loaded.')

        # extract code of conduct content
        code_content = self._extract_document_content(config.code_path)
        logger.info('The Galactic Code of Conduct has been loaded.')

        # initialize supporting info object
        self.info = Info(
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

    # public methods
    def process_menu(self, menu_path: Path) -> List[Dish]:
        # TODO: implement this method
        pass