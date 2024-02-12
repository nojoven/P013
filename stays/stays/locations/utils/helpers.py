import json
import os
import asyncio
import httpx
from django.core.exceptions import ObjectDoesNotExist
from icecream import ic
from cities_light.models import Country
from django.core.cache import cache
from asgiref.sync import sync_to_async, async_to_sync
from stays.settings import NINJAS_API_KEY as napk
from datetime import datetime
from django.http import HttpResponse
from django_countries import countries as dj_countries


# Create the headers for the Ninjas API
NINJAS_API_HEADERS = {'X-Api-Key': napk}


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


def fill_context_general_informations(country_code: str, country_details_response: dict):

    country_details = country_details_response[0]

    # Format some details
    currency_code = list(country_details.get('currencies').keys())[0]
    currency_name = country_details.get('currencies').get(currency_code).get('name')
    currency_symbol = country_details.get('currencies').get(currency_code).get('symbol')
    native_name_code = list(country_details.get("name").get("nativeName").keys())[0]

    general_info = {}

    general_info['Currency'] = f"{currency_name} ({currency_code}) - {currency_symbol}"
    general_info['Latitude'] = country_details.get("latlng")[0] if country_details.get("latlng") else "N/A"
    general_info['Longitude'] = country_details.get("latlng")[1] if country_details.get("latlng") else "N/A"
    general_info['Official'] = country_details.get("name").get("official")
    general_info['Native'] = country_details.get("name").get("nativeName").get(native_name_code).get("official")
    general_info['Capital'] = country_details.get("capital")[0] if country_details.get("capital") else "N/A"
    general_info['Languages'] = list(country_details.get("languages", "").values())[0]
    general_info['Google'] = country_details.get("maps", "").get("googleMaps")
    general_info['OpenStreet'] = country_details.get("maps", "").get("openStreetMaps")
    general_info['coat_of_arms'] = country_details.get("coatOfArms", "").get("png", "")
    general_info['flag'] = country_details.get("flags", f"https://flagcdn.com/w320/{country_code}.png").get("png")

    return general_info

def append_ninjas_api_general_info(general_info_dict: dict, api_response: dict):
    # Start processing Ninjas API responses
    country_data_ninjas = api_response[0]

    for key in country_data_ninjas:
        if key == "currency":
            continue

        # If the key is not already in the context, add it
        if key not in general_info_dict and key != "iso2" and "gdp not in key":
            general_info_dict[key.capitalize()] = country_data_ninjas.get(key)
        
        if key == "iso2":
            general_info_dict["ISO_2_Code"] = country_data_ninjas.get(key)
        
        if "rowth" in key or "rate" in key:
            general_info_dict[key.capitalize()] = f'{country_data_ninjas.get(key)} %'
        
        if "gdp" in key and len(key.split("_")) > 1:
            gdp_new_key = key.capitalize().replace("gdp", "GDP")
            general_info_dict[gdp_new_key] = country_data_ninjas.get(key)

        if "Gdp" in key and len(key.split("_")) > 1:
            if key.startswith("Gdp") or key.startswith("gdp"):
                updated_key = key.replace("gdp", "GDP")
                general_info_dict[updated_key] = country_data_ninjas.get(key)
            else:
                updated_key = key.capitalize().replace("gdp", "GDP")
                general_info_dict[updated_key] = country_data_ninjas.get(key)

        if key == "GDP":
            general_info_dict["GDP"] = country_data_ninjas.get(key)
        return general_info_dict



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

async def fetch_air_weather_time(general_info: dict):

    # Call the second async function and wait for it to finish
    if general_info.get("Capital"):

        additional_responses = await fetch_additional_data(general_info["Capital"], NINJAS_API_HEADERS)
        ic(additional_responses)
        # Unpack the responses
        air_quality_ninjas_api_response, weather_ninjas_api_response, world_time_ninjas_api_response = additional_responses
    
        # Extract the wanted collections from the responses
        air_quality_json = air_quality_ninjas_api_response.json()
        weather_json = weather_ninjas_api_response.json()
        world_time_json = world_time_ninjas_api_response.json()

        return {
            "air": air_quality_json,
            "weather": weather_json,
            "time": world_time_json
        }

def add_air_to_context(air_dict):
    if air_dict and "overall_aqi" in air_dict:
        air_dict["Overall"] = air_dict.get("overall_aqi")
        del air_dict["overall_aqi"]
    return air_dict

def add_weather_to_context(weather_dict):
    if not len(weather_dict) or weather_dict is None:
        return {}

    # Mapping dictionary
    key_mapping = {
        'cloud_pct': 'Clouds',
        'feels_like': 'Perceived',
        'humidity': 'Humidity',
        'max_temp': 'Max',
        'min_temp': 'Min',
        'sunrise': 'Sunrise',
        'sunset': 'Sunset',
        'temp': 'Temperature',
        'wind_degrees': 'Wind - Degrees',
        'wind_speed': 'Wind - Speed'
    }
    formatted_weather_json = {}

    # Improve format of the weather values
    for wkey, value in weather_dict.items():
        if wkey in key_mapping:
            new_key = key_mapping.get(wkey).capitalize()  # Get the new key from the mapping, or use the old key if not found
            if new_key in ['Clouds', 'Humidity']:
                new_value = f'{value} %'
            elif new_key in ['Perceived', 'Max', 'Min', 'Temperature']:
                new_value = f'{value} °C'
            elif new_key == 'Wind - degrees':
                new_key = 'Wind - Degrees'
                new_value = f'{value}°'
            elif new_key == 'Wind - speed':
                new_key = 'Wind - Speed'
                new_value = f'{value} km/h'
            elif new_key == 'Sunrise' or new_key == 'Sunset':
                # Convert the timestamp to a datetime object
                dt_object = datetime.fromtimestamp(value)

                # Format the datetime object as a string
                new_value = dt_object.strftime("%H:%M:%S")
            else:
                new_value = value
            formatted_weather_json[new_key] = new_value
        else:
            ic(wkey)
            ic(f"{wkey} not in key_mapping")
    return formatted_weather_json

def add_time_to_context(time_dict):
    if not time_dict:
        return {}
    return {
        "Local_Time": time_dict.get("datetime"),
        "Time_Zone": time_dict.get("timezone")
    }

def validate_country_code(country_code):
    if not isinstance(country_code, str) or len(country_code) < 2:
        ic(f"Lentgh of {len(country_code)} is less than 2")
        return HttpResponse("Probable invalid code in the link url. Please inform our support team.", status=400)
    
    if country_code.isdigit() \
        or "." in country_code and country_code.isdigit() \
            or "," in country_code and country_code.isdigit():
        return HttpResponse("Invalid country code. Please inform our support team.", status=400)

    if len(country_code) == 2:
        ic("lenght of country_code is 2")
        # Check if the country code exists in django-countries
        if country_code.upper() not in dj_countries:
            ic("Not in django-countries")
            return HttpResponse("Invalid country code.", status=400)
    if len(country_code) > 2:
        # Check if the country name exists in django-cities-light
        exists = Country.objects.filter(name=country_code.capitalize()).exists()
        ic(exists)
        if not exists:
            ic("Not found with the  two first letters of the country name. Checking with the full name.")
            return HttpResponse("Invalid country name.", status=400)
        else:
            country_code = country_code[:2].upper()


async def send_http_requests(country_code):
    # Call the async function and wait for it to finish
    responses = await fetch_country_data(country_code, NINJAS_API_HEADERS)
    # Unpack the responses
    country_details, country_details_ninjas = responses
    if country_details.status_code != 200 or country_details_ninjas.status_code != 200:
        return HttpResponse("Invalid country code.", status=400)
    
    return {
        "country_details": country_details.json(),
        "country_details_ninjas": country_details_ninjas.json()
    }