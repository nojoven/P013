import pytest
from unittest.mock import Mock, patch
from locations.utils.helpers import find_cities_light_country_name_with_code
from django.core.exceptions import ObjectDoesNotExist

def test_find_cities_light_country_name_with_code():
    with patch('cities_light.models.Country.objects.get') as mock_get:
        # Test when country is found
        mock_country = Mock()
        mock_country.name = 'Test Country'
        mock_get.return_value = mock_country

        assert find_cities_light_country_name_with_code('TC') == 'Test Country'

        # # Test when country is not found
        # mock_get.side_effect = ObjectDoesNotExist

        assert find_cities_light_country_name_with_code('XX') is None
        assert find_cities_light_country_name_with_code(None) is None
        assert find_cities_light_country_name_with_code(687743) is None