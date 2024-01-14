from django.contrib.auth import views as authentication_views
from django.urls import path, include
from users import views



app_name = 'users'

urlpatterns = [
    path("signup", views.CreateProfileView.as_view(), name="signup"),
    path("login", views.AccountLoginView.as_view(template_name='signin.html'), name='login'),
    path("logout", authentication_views.LogoutView.as_view(template_name='signout.html'), name='logout'),
    path("account/<slug:slug>", views.AccountDetailsView.as_view(), name="account"),
    path("account/<slug:slug>/stays", views.ProfileStaysListView.as_view(), name="stays"),
    path("account/<slug:slug>/publish", views.PublishView.as_view(), name="publish"),
    path("account/<slug:slug>/settings", views.UpdateAccountView.as_view(), name="settings"),
    path("account/<slug:slug>/delete", views.DeleteProfileView.as_view(), name="delete_account"),
    path("", include('allauth.urls')),
]
