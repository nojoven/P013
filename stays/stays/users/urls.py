from django.contrib.auth import views as authentication_views
from django.urls import path, include
from users import views



app_name = 'users'

urlpatterns = [
    path("", include('allauth.urls')),
    # path('publish', core_forms.PublishForm.as_view()),
    path("myaccount/<slug:slug>", views.AccountDetailsView.as_view(), name="myaccount"),
    path("settings/<slug:slug>", views.UpdateAccountView.as_view(), name="settings"),
    path("signup", views.CreateProfileView.as_view(), name="signup"),
    path("login", views.AccountLoginView.as_view(template_name='signin.html'), name='login'),
    path("logout", authentication_views.LogoutView.as_view(template_name='signout.html'), name='logout'),
]