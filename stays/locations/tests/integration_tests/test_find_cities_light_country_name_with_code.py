from django.test import TestCase
from locations.utils.helpers import find_cities_light_country_name_with_code
from cities_light.models import Country


class TestFindCitiesLightCountryNameWithCode(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        Country.objects.create(name="Test Country", code2="TC")

    def test_find_cities_light_country_name_with_code(self):
        # Test when country is found
        assert find_cities_light_country_name_with_code("TC") == "Test Country"

        # Test when country is not found
        assert find_cities_light_country_name_with_code("XX") is None
        assert find_cities_light_country_name_with_code(48452347) is None
