import pytest
from django.http import HttpRequest
from users.utils import uuid_generator
from stays.api import is_profile_online, get_names_from_country_code
from django.conf import settings
# Configure Django settings
settings.configure()


test_slug = uuid_generator()


def test_is_profile_online(mocker):
    slug = test_slug
    # Setup
    request = HttpRequest()
    request.META = {'HTTP_X_FORWARDED_FOR': '127.0.0.1'}
    mock_profile = mocker.patch('users.models.Profile.objects.get')
    mock_profile.return_value = mocker.MagicMock(is_online=True)

    # Call the function
    response = is_profile_online(request, slug)

    # Check the result
    assert response.status_code == 200
    assert response.content.decode() == '{"is_online": true}'

    # Check that the mock was called with the correct slug
    mock_profile.assert_called_once_with(slug=slug)


def test_get_names_from_country_code(mocker):
    # Setup
    country_code = 'US'
    request = HttpRequest()
    mock_stay_country = mocker.patch('locations.models.StayCountry.objects.get')
    mock_stay_country.return_value = mocker.MagicMock(country_name='United States', continent_name='North America')

    # Call the function
    response = get_names_from_country_code(request, country_code)

    # Check the result
    assert response == {"country": 'United States', "continent": 'North America'}

    # Check that the mock was called with the correct country code
    mock_stay_country.assert_called_once_with(country_code_of_stay=country_code)