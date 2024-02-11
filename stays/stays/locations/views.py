from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from icecream import ic
from stays.settings import NINJAS_API_KEY as napk
import httpx
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from django_countries import countries as dj_countries

from cities_light.models import Country
from django.contrib.auth.decorators import login_required
from locations.utils.helpers import fetch_country_data, fetch_additional_data, ninjas_api_headers



# @login_required
@sync_to_async
def country_view(request, country_code):
    # Get country data from Restcountries API
    ic("country_code: ", country_code)

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

    # Create the context dictionary
    context = {}

    

    # Call the async function and wait for it to finish
    responses = async_to_sync(fetch_country_data)(country_code, ninjas_api_headers)
    # Unpack the responses
    country_details, country_details_ninjas = responses
    ic(responses)
    if country_details.status_code != 200 or country_details_ninjas.status_code != 200:
        ic(404)
        return HttpResponse("Invalid country code.", status=400)

    # Process The response from Restcountries API
    country_details = country_details.json()[0]
    # Format the currency details
    currency_code = list(country_details.get('currencies').keys())[0]
    currency_name = country_details.get('currencies').get(currency_code).get('name')
    currency_symbol = country_details.get('currencies').get(currency_code).get('symbol')

    # Extract the native name code (depends on the country in your httpp request)
    native_name_code = list(country_details.get("name").get("nativeName").keys())[0]

    context["general_information"] = {
        'Latitude': country_details.get("latlng")[0] if country_details.get("latlng") else "N/A",
        'Longitude': country_details.get("latlng")[1] if country_details.get("latlng") else "N/A",
        'Official': country_details.get("name").get("official"),
        'Native': country_details.get("name").get("nativeName").get(native_name_code).get("official"),
        'Capital': country_details.get("capital")[0] if country_details.get("capital") else "N/A",
        "Currency": f"{currency_name} ({currency_code}) - {currency_symbol}",
        'Languages': list(country_details.get("languages", "").values())[0],
        'Google': country_details.get("maps", "").get("googleMaps"),
        'OpenStreet': country_details.get("maps", "").get("openStreetMaps"),
        'coat_of_arms': country_details.get("coatOfArms", "").get("png", ""),
        'flag': country_details.get("flags", f"https://flagcdn.com/w320/{country_code}.png").get("png"),
    }

    
    # Start processing Ninjas API responses
    country_data_ninjas = country_details_ninjas.json()[0]
    
    for key in country_data_ninjas:
        if key == "currency":
            continue

        # If the key is not already in the context, add it
        if key not in context["general_information"] and key != "iso2" and "gdp not in key":
            context["general_information"][key.capitalize()] = country_data_ninjas.get(key)
        
        if key == "iso2":
            context["general_information"]["ISO_2_Code"] = country_data_ninjas.get(key)
        
        if "rowth" in key or "rate" in key:
            context["general_information"][key.capitalize()] = f'{country_data_ninjas.get(key)} %'
        
        if "gdp" in key and len(key.split("_")) > 1:
            gdp_new_key = key.capitalize().replace("gdp", "GDP")
            context["general_information"][gdp_new_key] = country_data_ninjas.get(key)

        if "Gdp" in key and len(key.split("_")) > 1:
            if key.startswith("Gdp") or key.startswith("gdp"):
                updated_key = key.replace("gdp", "GDP")
                context["general_information"][updated_key] = country_data_ninjas.get(key)
            else:
                updated_key = key.capitalize().replace("gdp", "GDP")
                context["general_information"][updated_key] = country_data_ninjas.get(key)

        if key == "GDP":
            context["general_information"]["GDP"] = country_data_ninjas.get(key)

    # Call the second async function and wait for it to finish
    if context["general_information"].get("Capital"):
        additional_responses = async_to_sync(fetch_additional_data)(context["general_information"]["Capital"], country_code, ninjas_api_headers)
        ic(additional_responses)
        # Unpack the responses
        air_quality_ninjas_api_response, weather_ninjas_api_response, world_time_ninjas_api_response = additional_responses
    
        # Extract the wanted collections from the responses
        air_quality_json = air_quality_ninjas_api_response.json()
        weather_json = weather_ninjas_api_response.json()
        world_time_json = world_time_ninjas_api_response.json()

    # Air Quality
    if air_quality_json and "overall_aqi" in air_quality_json:
        air_quality_json["Overall"] = air_quality_json.get("overall_aqi")
        del air_quality_json["overall_aqi"]
        context["air"] = air_quality_json

    # Weather
    if weather_json:
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
        for wkey, value in weather_json.items():
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
        context["weather"] = formatted_weather_json

    # World Time
    if world_time_json:
        context["country_time"] = {"Local_Time": world_time_json.get("datetime"), "Time_Zone": world_time_json.get("timezone")}

    ic("output")
    ic(type(context))
    # ic(context)
    return render(request, 'country.html', context)
    # return HttpResponse("OK", status=200)