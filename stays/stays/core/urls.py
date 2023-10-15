from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # /home
    path("", views.home, name="home"),
]
