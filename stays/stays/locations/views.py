from django.shortcuts import render
import requests
from icecream import ic
from stays.settings import NINJAS_API_KEY as napk
from stays.settings import MAPBOX_TOKEN as mpt



# Create your views here.


    
def country_view(request, country_code):
    # Get country data from Restcountries API
    response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
    country_details = response.json()[0]
    google_maps_url = country_details.get("maps")["googleMaps"] if country_details.get("maps") else None
    currency = country_details.get("currencies")
    headers = {'X-Api-Key': napk}
    response_ninjas = requests.get(f'https://api.api-ninjas.com/v1/country?name={country_code}', headers=headers)
    country_details_ninjas = response_ninjas.json()

    # if response_ninjas.text:
    #     country_details_ninjas = response_ninjas.json()[0]  # Access the first item in the list
    # else:
    #     country_details_ninjas = {}

    context = {
        'country_lat': country_details.get("latlng")[0],
        'country_lon': country_details.get("latlng")[1],
        'country_name': country_details.get("name"),
        'country_capital': country_details.get("capital"),
        'country_currency': currency,
        'country_population': country_details_ninjas[0].get("population"),
        'country_area': country_details_ninjas[0].get("surface_area"),
        'country_languages': country_details.get("languages", ""),
        'google_maps_url': google_maps_url,
        'gdp': country_details_ninjas[0].get("gdp"),
        'unemployment': country_details_ninjas[0].get("unemployment"),
        'gdp_growth': country_details_ninjas[0].get("gdp_growth"),
        'infant_mortality': country_details_ninjas[0].get("infant_mortality"),
        'fertility': country_details_ninjas[0].get("fertility"),
        'urban_pop_rate': country_details_ninjas[0].get("urban_population_growth"),
    }

    return render(request, 'country.html', context)