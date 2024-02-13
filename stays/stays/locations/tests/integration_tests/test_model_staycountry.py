
from django.test import TestCase
from locations.models import StayCountry

class StayCountryModelTest(TestCase):
    def test_can_create_stay_country(self):
        stay_country = StayCountry.objects.create(
            continent_name='Asia',
            country_name='Japan',
            country_code_of_stay='JP'
        )
        self.assertEqual(stay_country.continent_name, 'Asia')
        self.assertEqual(stay_country.country_name, 'Japan')
        self.assertEqual(stay_country.country_code_of_stay, 'JP')