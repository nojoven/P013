"""
URL configuration for stays project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as authentication_views
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

from users import views as user_views


urlpatterns = [
    path("admin", admin.site.urls),
    path("", include("core.urls")),
    path("", include("users.urls")),
    #path("signup", user_views.register, name="register"),
    re_path(r'^watchman/', include('watchman.urls')),
        path("login", authentication_views.LoginView.as_view(template_name='signin.html'), name='login'),
        path("logout", authentication_views.LogoutView.as_view(template_name='signout.html'), name='logout'),
] + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
)
