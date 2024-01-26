from django.http import HttpResponse
from django.shortcuts import render
import requests
from datetime import datetime
from icecream import ic
from stays.settings import NINJAS_API_KEY as napk
from stays.settings import MAPBOX_TOKEN as mpt



# Create your views here.


def country_view(request, country_code):
    # Get country data from Restcountries API
    if not isinstance(country_code, str) or len(country_code) < 2:
        return HttpResponse("Invalid link url. Please inform our support team.", status=400)
    if len(country_code) > 2:
        country_code = country_code[:2].upper()
    response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
    country_details = response.json()[0]

    native_name_code = list(country_details.get("name").get("nativeName").keys())[0]
    country_data = {
        'Latitude': country_details.get("latlng")[0],
        'Longitude': country_details.get("latlng")[1],
        'Official': country_details.get("name").get("official"),
        'Native': country_details.get("name").get("nativeName").get(native_name_code).get("official"),
        'Capital': country_details.get("capital")[0],
        # 'Currency': f"{country_details.get('currencies').get('name')} ({country_details.get('currencies').get('symbol')})",
        'Languages': list(country_details.get("languages", "").values())[0],
        'Google': country_details.get("maps", "").get("googleMaps"),
        'OpenStreet': country_details.get("maps", "").get("openStreetMaps"),
        'coat_of_arms': country_details.get("coatOfArms", "").get("png", ""),
        'flag': country_details.get("flags", f"https://flagcdn.com/w320/{country_code}.png").get("png"),
    }

    # ninjas api
    headers = {'X-Api-Key': napk}
    response_ninjas = requests.get(f'https://api.api-ninjas.com/v1/country?name={country_code}', headers=headers)
    country_details_ninjas = response_ninjas.json()

    for key in country_details_ninjas[0]:
        # If the key is not already in the context, add it
        if key not in country_data and key != "iso2" and "gdp not in key" and key != "Currency":
            country_data[key.capitalize()] = country_details_ninjas[0].get(key)
        
        if key == "iso2":
            country_data["ISO_2_Code"] = country_details_ninjas[0].get(key)
            
        if "gdp" in key and len(key.split("_")) > 1:
            gdp_new_key = key.capitalize().replace("gdp", "GDP")
            country_data[gdp_new_key] = country_details_ninjas[0].get(key)

        if "Gdp" in key and len(key.split("_")) > 1:
            if key.startswith("Gdp") or key.startswith("gdp"):
                updated_key = key.replace("gdp", "GDP")
                country_data[updated_key] = country_details_ninjas[0].get(key)
            else:
                updated_key = key.capitalize().replace("gdp", "GDP")
                country_data[updated_key] = country_details_ninjas[0].get(key)

        if key == "GDP":
            country_data["GDP"] = country_details_ninjas[0].get(key)

    # ninjas overwrites restcountries "Currency"
    # Format the currency details
    ic(country_details.get('currencies'))
    currency_code = list(country_details.get('currencies').keys())[0]
    currency_name = country_details.get('currencies').get(currency_code).get('name')
    currency_symbol = country_details.get('currencies').get(currency_code).get('symbol')
    country_data["Currency"] = f"{currency_name} ({currency_code}) - {currency_symbol}"
    
    
    context = {"general_information": country_data}
    
    # Air Quality
    if country_data.get("Capital"):
        air_quality_ninjas_api_response = requests.get(f'https://api.api-ninjas.com/v1/airquality?city={country_data["Capital"]}', headers=headers)
        air_quality_json = air_quality_ninjas_api_response.json()
        if air_quality_json:
            air_quality_json["Overall"] = air_quality_json.get("overall_aqi")
            del air_quality_json["overall_aqi"]
            context["air"] = air_quality_json

    # Timezone
    # timezone_ninjas_api_response = requests.get(f'https://api.api-ninjas.com/v1/timezone?country={country_code}', headers=headers)
    # timezone_json = timezone_ninjas_api_response.json()[0]
    # if timezone_json:
    #     context["Timezone"] = timezone_json.get("timezone")
    
    # Weather                                         
    weather_ninjas_api_response = requests.get(f'https://api.api-ninjas.com/v1/weather?city={country_data["Capital"]}&country={country_code}', headers=headers)
    weather_json = weather_ninjas_api_response.json()
    
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

    for key, value in weather_json.items():
        new_key = key_mapping.get(key).capitalize()  # Get the new key from the mapping, or use the old key if not found
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
    
    context["weather"] = formatted_weather_json

    # World Time
    world_time_ninjas_api_response = requests.get(f"https://api.api-ninjas.com/v1/worldtime?city={country_data['Capital']}&country={country_code}", headers=headers)
    world_time_json = world_time_ninjas_api_response.json()
    if world_time_json:
        ic(world_time_json)
        context["country_time"] = {"Local_Time": world_time_json.get("datetime"), "Time_Zone": world_time_json.get("timezone")}


    return render(request, 'country.html', context)
