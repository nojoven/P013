from ninja import NinjaAPI, Router
from throttle.decorators import throttle
from django.http import JsonResponse

from users.models import Profile
from locations.models import StayCountry


# from django_currentuser.middleware import (
#     get_current_user,
#     get_current_authenticated_user)

api = NinjaAPI()

@throttle(zone='default')
@api.get("/isonline/{slug}/")
def is_profile_online(request, slug: str):
    profile = Profile.objects.get(slug=slug)
    return JsonResponse({'is_online': profile.is_online})


@api.get("/geodata/countries/country/{country_code}/")
def get_names_from_country_code(request, country_code: str):
    stay_country = StayCountry.objects.get(country_code_of_stay=country_code)
    return {"country": stay_country.country_name, "continent": stay_country.continent_name}
