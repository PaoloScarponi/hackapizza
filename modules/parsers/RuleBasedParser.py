# external modules import
import re
from typing import List, Dict
from Levenshtein import distance

# internal modules import
from ..enums import Planet, TechniqueCategory
from ..templates import Ingredient, IngredientsList, Technique, TechniquesList


# class definition
class RuleBasedParser:

    # non-public methods
    @staticmethod
    def _fuzzy_substring_match(substring: str, text: str, max_distance: int) -> bool:
        sub_len = len(substring)
        for i in range(len(text) - sub_len + 1):
            if distance(substring, text[i:i + sub_len]) <= max_distance:
                return True

        return False

    # public methods
    @staticmethod
    def extract_restaurant_name(input_text: List[str]) -> str:
        return re.sub(r'Ristorante:|Ristorante "|"', '', input_text[0]).strip()

    @staticmethod
    def extract_restaurant_planet(input_text: List[str]) -> Planet:
        restaurant_planet = Planet.UNDISCLOSED
        r_info = '\n'.join(input_text).lower()
        for p in Planet:
            if p.value.lower() in r_info:
                restaurant_planet = p
                break

        return restaurant_planet

    @staticmethod
    def extract_dish_ingredients(input_text: List[str]) -> IngredientsList:
        ingredients_list, start_flag = [], False
        for line in input_text:
            if distance(line.lower(), 'tecniche') <= 1 or distance(line.lower(), 'techniques') <= 1:
                break
            if start_flag:
                ingredients_list.append(re.sub(r'[\r\n]+', '', line))
            if distance(line.lower(), 'ingredienti') <= 1:
                start_flag = True

        return IngredientsList(items=[Ingredient(name=x) for x in ingredients_list])

    @staticmethod
    def extract_dish_techniques_v1(input_text: List[str], additional_info: Dict[str, str]) -> TechniquesList:
        techniques_list, start_flag = [], False
        for line in input_text:
            if start_flag:
                technique_name = re.sub(r'[\r\n]+', '', line).strip().lower()
                for tn, tc in additional_info.items():
                    if distance(technique_name, tn.lower()) <= 2:
                        techniques_list.append(
                            Technique(
                                name=tn,
                                category=TechniqueCategory(tc)
                            )
                        )
            if distance(line.lower(), 'tecniche') <= 1 or distance(line.lower(), 'techniques') <= 1:
                start_flag = True

        return TechniquesList(items=techniques_list)

    @classmethod
    def extract_dish_techniques_v2(cls, input_text: List[str], additional_info: Dict[str, str]) -> TechniquesList:
        techniques_list = []
        input_str = '\n'.join(input_text).lower()
        for tn, tc in additional_info.items():
            if cls._fuzzy_substring_match(substring=tn.lower(), text=input_str, max_distance=3):
                techniques_list.append(
                    Technique(
                        name=tn,
                        category=TechniqueCategory(tc)
                    )
                )

        return TechniquesList(items=techniques_list)
