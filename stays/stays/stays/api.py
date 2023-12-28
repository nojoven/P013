from ninja import NinjaAPI
from throttle.decorators import throttle

api = NinjaAPI()

@throttle(zone='default')
@api.get("/hello")
def hello(request):
    return "Hello world"