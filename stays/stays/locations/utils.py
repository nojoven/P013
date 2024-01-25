import json
import os
from django.core.exceptions import ObjectDoesNotExist
from icecream import ic
from cities_light.models import Country


def get_continent_from_code(continent_code: str):
    # current_dir = os.path.dirname(os.path.abspath(__file__))

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file_path = os.path.join(base_dir, 'locations', 'continents.json')
    with open(json_file_path) as json_file:
        mapping = json.load(json_file)
        return mapping.get(continent_code)


def find_cities_light_country_name_with_code(country_code: str):
    ic(f"Searching for country with code: '{country_code}'")
    try:
        country = Country.objects.get(code2=country_code)
        ic(f"Found country: {country.name}")
        return country.name
    except ObjectDoesNotExist:
        ic(f"No country found with code: '{country_code}'")
        return None

def find_cities_light_continent_with_country_code(country_code: str):
    return Country.objects.get(code2=country_code).continent
