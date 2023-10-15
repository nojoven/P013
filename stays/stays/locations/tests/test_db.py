from django.test import TestCase
from ..models import LocationCategory, Location, LocationWebData, LocationHasProfileActivity

# Create your tests here.
def test_can_select_all_location_categories():
    categories  = LocationCategory.objects.all()
    assert categories is not None

def test_can_select_all_locations():
    locations  = Location.objects.all()
    assert locations is not None


def test_can_select_all_location_web_data():
    web_data  = LocationWebData.objects.all()
    assert web_data is not None


def test_can_select_all_location_profiles_activity():
    activities  = LocationHasProfileActivity.objects.all()
    assert activities is not None

