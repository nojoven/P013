from django.http import HttpRequest

from stays.api import is_profile_online
from stays.utils.common_helpers import uuid_generator

test_slug = uuid_generator()


def test_is_profile_online(mocker):
    slug = test_slug
    # Setup
    request = HttpRequest()
    request.META = {"HTTP_X_FORWARDED_FOR": "127.0.0.1"}
    mock_profile = mocker.patch("users.models.Profile.objects.get")
    mock_profile.return_value = mocker.MagicMock(is_online=True)

    # Call the function
    response = is_profile_online(request, slug)

    # Check the result
    assert response.status_code == 200
    assert response.content.decode() == '{"is_online": true}'

    # Check that the mock was called with the correct slug
    mock_profile.assert_called_once_with(slug=slug)
