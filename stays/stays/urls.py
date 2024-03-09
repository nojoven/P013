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
from django.urls import include, path

from stays.api import api
from stays.utils.errors_helpers import random_error_handler

# from machina import urls as machina_urls


urlpatterns = [
    path("admin", admin.site.urls),
    path("admin/defender/", include("defender.urls")),
    path("", include("core.urls")),
    path("", include("locations.urls")),
    path("", include("users.urls")),
    path("api/", api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "stays.urls.handler400"
handler401 = "stays.urls.handler401"
handler403 = "stays.urls.handler403"
handler404 = "stays.urls.handler404"
handler410 = "stays.urls.handler410"
handler418 = "stays.urls.handler418"
handler429 = "stays.urls.handler429"
handler500 = "stays.urls.handler500"
handler503 = "stays.urls.handler503"
handler504 = "stays.urls.handler504"


# Error handlers WHEN DEBUG=TRUE
def handler400(request, exception):
    return random_error_handler(request, 400)


def handler401(request, exception):
    return random_error_handler(request, 401)


def handler403(request, exception):
    return random_error_handler(request, 403)


def handler404(request, exception):
    return random_error_handler(request, 404)


def handler410(request, exception):
    return random_error_handler(request, 410)


def handler418(request, exception):
    return random_error_handler(request, 418)


def handler429(request, exception):
    return random_error_handler(request, 429)


def handler500(request):
    return random_error_handler(request, 500)


def handler503(request, exception):
    return random_error_handler(request, 503)


def handler504(request, exception):
    return random_error_handler(request, 504)


def handlerOther(request, exception=None):
    # 520 is an example. You can use any HTTP status code that you want to handle.
    return random_error_handler(request, 520)
