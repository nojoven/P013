import pytest
from django.http import HttpRequest
from users.utils import uuid_generator
from stays.api import is_profile_online
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
