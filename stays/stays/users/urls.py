from django.urls import path
from users import views


app_name = 'users'

urlpatterns = [
    # /home
    path("signup", views.register, name="register"),
    #path("signup", views.CreateProfileView.as_view(), name="signup"),
]