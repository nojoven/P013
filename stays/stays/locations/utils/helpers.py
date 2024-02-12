import json
import os
import asyncio
import httpx
from django.core.exceptions import ObjectDoesNotExist
from icecream import ic
from cities_light.models import Country
from django.core.cache import cache
from stays.settings import NINJAS_API_KEY as napk
# Create the headers for the Ninjas API
ninjas_api_headers = {'X-Api-Key': napk}


def get_continent_from_code(continent_code: str):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file_path = os.path.join(base_dir, 'continents.json')
    with open(json_file_path) as json_file:
        mapping = json.load(json_file)
        return mapping.get(continent_code)


def find_cities_light_country_name_with_code(country_code: str):
    try:
        country = Country.objects.get(code2=country_code)
        return country.name
    except ObjectDoesNotExist:
        ic(f"No country found with code: '{country_code}'")
        return None


def find_cities_light_continent_with_country_code(country_code: str):
    return Country.objects.get(code2=country_code).continent


async def fetch_country_data(country_code, headers):
    if country_code is None:
        raise ValueError("The country_code parameter cannot be None.")
    if not len(country_code):
        raise ValueError("The country_code parameter cannot be empty.")
    if headers is None:
        raise ValueError("The headers parameter cannot be None.")
    if not isinstance(headers, dict):
        raise TypeError("The headers parameter must be a dictionary.")
    if not len(headers):
        raise ValueError("The headers dictionary cannot be empty.")
    if "X-Api-Key" not in headers:
        raise KeyError("The headers dictionary must contain an 'X-Api-Key' key.")
    if headers["X-Api-Key"] != napk or not headers["X-Api-Key"]:
        raise ValueError("The 'X-Api-Key' header value does not match the expected value.")
    if  len(headers["X-Api-Key"]) < 30:
        raise ValueError("Invalid API key.")

    # Create a unique cache key for this function and country_code
    cache_key = f'country_data_{country_code}'

    # Try to get the response from the cache
    responses = cache.get(cache_key)

    # If the response is not in the cache, fetch it
    if responses is None:
        ic("Fetching country data")
        async with httpx.AsyncClient(verify=False) as client:
            url1 = f'https://restcountries.com/v3.1/alpha/{country_code}'
            url2 = f'https://api.api-ninjas.com/v1/country?name={country_code}'

            responses = await asyncio.gather(
                client.get(url1),
                client.get(url2, headers=headers),
            )

        # Store the response in the cache
        cache.set(cache_key, responses)
    ic(type(responses))
    ic(responses)
    return responses


async def fetch_additional_data(capital, headers):

    if not isinstance(capital, str):
        raise TypeError("The 'capital' parameter must be a string.")

    if not len(capital):
        raise ValueError("Empty value of required parameters: 'capital'")

    if headers and not capital:
        raise ValueError("Invalid required parameters: 'capital'")

    if headers and not isinstance(headers, dict):
        raise TypeError("The 'headers' parameter must be a dictionary.")

    if not headers:
        raise ValueError("Invalid required parameters: 'headers'")

    # Create a unique cache key for this function, capital and country_code
    cache_key = f'additional_data_{capital}'

    # Try to get the response from the cache
    responses = cache.get(cache_key)

    # If the response is not in the cache, fetch it
    if responses is None:
        ic("Fetching additional data")
        async with httpx.AsyncClient(verify=False) as client:
            url3 = f'https://api.api-ninjas.com/v1/airquality?city={capital}'
            url4 = f'https://api.api-ninjas.com/v1/weather?city={capital}'
            url5 = f"https://api.api-ninjas.com/v1/worldtime?city={capital}"

            responses = await asyncio.gather(
                client.get(url3, headers=headers),
                client.get(url4, headers=headers),
                client.get(url5, headers=headers)
            )
            # Check the status code of the responses
            for response in responses:
                if response.status_code >= 400:
                    raise Exception(f'API request failed with status code {response.status_code}')
        # Store the response in the cache
        cache.set(cache_key, responses)
    else:
        ic("Responses found in cache")
    ic(type(responses))

    return responses
