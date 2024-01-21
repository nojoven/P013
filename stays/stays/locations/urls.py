from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    # Other routes...
    path('country/<str:country_code>', views.country_view, name='country'),
]