from django.urls import path
from locations import views

app_name = 'locations'

urlpatterns = [
    path('country/<str:country_code>', views.country_view, name='country'),
]
