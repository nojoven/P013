from django.shortcuts import render
from icecream import ic
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from locations.utils.helpers import (
    fill_context_general_informations,
    append_ninjas_api_general_info,
    fetch_air_weather_time,
    add_air_to_context,
    add_weather_to_context,
    add_time_to_context,
    validate_country_code,
    send_http_requests
)


# @login_required
async def country_view(request, country_code):
    # Get country data from Restcountries API
    ic("country_code: ", country_code)

    error_in_code = await validate_country_code(country_code)
    if error_in_code is not None:
        return error_in_code


    # Create the context dictionary
    context = {}

    response_collection = await send_http_requests(country_code)
    ic(response_collection.keys())
    country_details = response_collection["country_details"]
    country_details_ninjas = response_collection["country_details_ninjas"]

    context["general_information"] = fill_context_general_informations(country_code, country_details)


    context["general_information"] = append_ninjas_api_general_info(context["general_information"], country_details_ninjas)
    
    environment_data = await fetch_air_weather_time(context["general_information"])
    air_quality_json = environment_data.get("air")
    weather_json = environment_data.get("weather")
    world_time_json = environment_data.get("time")

    # Air Quality
    context["air"] = add_air_to_context(air_quality_json)

    # Weather
    context["weather"] = add_weather_to_context(weather_json)

    # World Time
    context["country_time"] = add_time_to_context(world_time_json)

    ic("output")
    ic(type(context))
    # ic(context)
    return render(request, 'country.html', context)