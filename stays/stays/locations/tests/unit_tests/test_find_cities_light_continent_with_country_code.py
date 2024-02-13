import pytest
from unittest.mock import Mock, patch
from locations.utils.helpers import find_cities_light_continent_with_country_code
from django.core.exceptions import ObjectDoesNotExist


def test_find_cities_light_continent_with_country_code():
    with patch('cities_light.models.Country.objects.get') as mock_get:
        # Test lorsque le pays est trouvé
        mock_country = Mock()
        mock_country.continent = 'Test Continent'
        mock_get.return_value = mock_country

        assert find_cities_light_continent_with_country_code('TC') == 'Test Continent'

        # Réinitialiser le mock pour le prochain test
        mock_get.reset_mock()

        # Test lorsque le pays n'est pas trouvé
        mock_get.side_effect = ObjectDoesNotExist

        with pytest.raises(ObjectDoesNotExist):
            find_cities_light_continent_with_country_code('XX')
            find_cities_light_continent_with_country_code(None)
            find_cities_light_continent_with_country_code(687743)

        mock_get.assert_called_once_with(code2='XX')
