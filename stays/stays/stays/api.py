from ninja import NinjaAPI, Router
from throttle.decorators import throttle
from django.http import JsonResponse

from users.models import Profile
from locations.models import StayCountry

api = NinjaAPI()

@throttle(zone='default')
@api.get("/isonline/{slug}/")
def is_profile_online(request, slug: str):
    profile = Profile.objects.get(slug=slug)
    return JsonResponse({'is_online': profile.is_online})
