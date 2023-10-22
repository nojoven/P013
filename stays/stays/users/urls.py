from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # /home
    path("signup", views.register, name="signup"),
]