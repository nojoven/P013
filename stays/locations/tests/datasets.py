from stays.settings import NINJAS_API_KEY as napk
# from django.core.cache import cache
# Constants for test cases
VALID_COUNTRY_CODES = ['US', 'FR', 'JP']
INVALID_COUNTRY_CODES = ['ZX', '00']
HEADERS = {'X-Api-Key': napk}

VALID_CAPITALS = ["Paris", "London", "Dakar"]
INVALID_CAPITALS = ["@freebox", "chhhhhhhhh", "ShangaiAbidjan"]
