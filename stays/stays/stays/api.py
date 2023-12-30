from ninja import NinjaAPI
from throttle.decorators import throttle

from django_currentuser.middleware import (
    get_current_user, 
    get_current_authenticated_user)

api = NinjaAPI()


@throttle(zone='default')
@api.get("/hello")
def hello(request):
    return "Hello world"
