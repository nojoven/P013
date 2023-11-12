from django.contrib.auth import views as authentication_views
from django.urls import path, include
from users import views



app_name = 'users'

urlpatterns = [
    path("", include('allauth.urls')),
    #path("account/<int:pk>", views.UpdateAccountView.as_view(), name="account"),
    path("myaccount", views.myaccount, name="myaccount"),
    #path("settings", views.mysettings, name="settings"),
    path("settings/<int:pk>", views.UpdateAccountView.as_view(), name="settings"),
    path("signup", views.CreateProfileView.as_view(), name="signup"),
    path("login", views.AccountLoginView.as_view(template_name='signin.html'), name='login'),
    path("logout", authentication_views.LogoutView.as_view(template_name='signout.html'), name='logout'),
]