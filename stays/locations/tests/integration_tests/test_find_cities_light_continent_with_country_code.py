import pytest
from django.test import TestCase
from locations.utils.helpers import find_cities_light_continent_with_country_code
from cities_light.models import Country


class TestFindCitiesLightContinentWithCountryCode(TestCase):
    def setUp(self):
        # Créer les données pour chaque test
        Country.objects.create(name="France", code2="FR", continent="EU")
        Country.objects.create(name="United States", code2="US", continent="NA")
        Country.objects.create(name="Canada", code2="CA", continent="NA")
        Country.objects.create(name="Australia", code2="AU", continent="OC")
        Country.objects.create(name="China", code2="CN", continent="AS")
        Country.objects.create(name="India", code2="IN", continent="AS")
        Country.objects.create(name="Brazil", code2="BR", continent="SA")
        Country.objects.create(name="Morocco", code2="MA", continent="AF")

    def test_find_cities_light_continent_with_country_code(self):
        # Test lorsque le pays est trouvé
        assert find_cities_light_continent_with_country_code("FR") == "EU"
        assert find_cities_light_continent_with_country_code("CA") == "NA"
        assert find_cities_light_continent_with_country_code("US") == "NA"
        assert find_cities_light_continent_with_country_code("CN") == "AS"
        assert find_cities_light_continent_with_country_code("IN") == "AS"
        assert find_cities_light_continent_with_country_code("BR") == "SA"
        assert find_cities_light_continent_with_country_code("AU") == "OC"
        assert find_cities_light_continent_with_country_code("MA") == "AF"

        # Test lorsque le pays n'est pas trouvé
        with pytest.raises(Country.DoesNotExist):
            find_cities_light_continent_with_country_code("XX")
            find_cities_light_continent_with_country_code(None)
            find_cities_light_continent_with_country_code(1284)
