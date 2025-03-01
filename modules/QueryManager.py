# external modules import
from typing import List

# internal modules import
from .enums import Planet
from .templates import AugmentedDish, Restaurant, License, Ingredient, Technique


# class definition
class QueryManager:
    """
    This class implements all the capabilities to query the Knowledge Base.

    """

    def __init__(self):
        # TODO: implement the object initialization routine loading/computing the following:
        #       * list of all augmented dish.
        #       * list of ingredients.
        #       * list of techniques.
        #       To prepare lists of planet we have to handle distances between them.
        #       To handle lists of licenses we have to understand levels.
        pass

    @staticmethod
    def filter_dishes_by_restaurant(input_dishes: List[AugmentedDish], restaurant: Restaurant) -> List[AugmentedDish]:
        return [ad for ad in input_dishes if restaurant.name == ad.restaurant.name]

    @staticmethod
    def filter_dishes_by_planet(input_dishes: List[AugmentedDish], planet: Planet) -> List[AugmentedDish]:
        return [ad for ad in input_dishes if planet == ad.restaurant.planet]

    @staticmethod
    def filter_dishes_by_chef_license(input_dishes: List[AugmentedDish], chef_license: License) -> List[AugmentedDish]:
        return [ad for ad in input_dishes if any(i == chef_license for i in ad.chef.licenses.items)]

    @staticmethod
    def filter_dishes_by_ingredient(input_dishes: List[AugmentedDish], ingredient: Ingredient, exclude_flag: bool) -> List[AugmentedDish]:
        if not exclude_flag:
            output_dishes = [ad for ad in input_dishes if any(i == ingredient for i in ad.dish.ingredients.items)]
        else:
            output_dishes = [ad for ad in input_dishes if not any(i == ingredient for i in ad.dish.ingredients.items)]

        return output_dishes

    @staticmethod
    def filter_dishes_by_technique(input_dishes: List[AugmentedDish], technique: Technique, exclude_flag: bool) -> List[AugmentedDish]:
        if not exclude_flag:
            output_dishes = [ad for ad in input_dishes if any(i == technique for i in ad.dish.techniques.items)]
        else:
            output_dishes = [ad for ad in input_dishes if not any(i == technique for i in ad.dish.techniques.items)]

        return output_dishes
