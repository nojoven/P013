from ninja import NinjaAPI, Router
from throttle.decorators import throttle
from django.http import JsonResponse

from users.models import Profile


from django_currentuser.middleware import (
    get_current_user, 
    get_current_authenticated_user)

api = NinjaAPI()

@throttle(zone='default')
@api.get("/isonline/{slug}/")
def hello(request, slug: str):
    profile = Profile.objects.get(slug=slug)
    return JsonResponse({'is_online': profile.is_online})
