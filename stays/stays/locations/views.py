from django.shortcuts import render
import requests

# Create your views here.

def country_view(request, country_code):
    # Get country data from World Bank API
    response = requests.get(f'http://api.worldbank.org/v2/country/{country_code}?format=json')
    country_data = response.json()

    context = {
        'country_data': country_data,
    }

    return render(request, 'country.html', context)