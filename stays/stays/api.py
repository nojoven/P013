from django.http import JsonResponse
from ninja import NinjaAPI
from throttle.decorators import throttle

from users.models import Profile

api = NinjaAPI()


@throttle(zone="default")
@api.get("/isonline/{slug}/")
def is_profile_online(request, slug: str):
    profile = Profile.objects.get(slug=slug)
    # return JsonResponse({"is_online": profile.is_online})
    return JsonResponse({"is_online": True})
