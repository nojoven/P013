from unittest.mock import MagicMock, patch

import pytest
from django.http import HttpResponse

from locations.utils.helpers import validate_country_code


@pytest.mark.asyncio
async def test_validate_country_code():
    # Mock Country.objects.filter
    mock_filter = MagicMock()
    mock_filter.exists.return_value = True
    with patch(
        "locations.utils.helpers.Country.objects.filter", return_value=mock_filter
    ):
        # Test with a non-string input
        response = await validate_country_code(123)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 400
        assert (
            response.content.decode()
            == "Invalid country code. Please inform our support team."
        )

        # Test with a string that is too short
        short_string = "U"
        response = await validate_country_code(short_string)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 400
        assert (
            response.content.decode()
            == "Probable invalid code in the link url. Please inform our support team."
        )

        # Test with a string that contains only digits
        string_with_digits = "123"
        response = await validate_country_code(string_with_digits)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 400
        assert (
            response.content.decode()
            == "Invalid country code. Please inform our support team."
        )

        # Test with a string that contains a period and only digits
        string_with_period_and_digits = "1.23"
        response = await validate_country_code(string_with_period_and_digits)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 400
        assert (
            response.content.decode()
            == "Invalid country code. Please inform our support team."
        )

    # Mock Country.objects.filter
    mock_filter = MagicMock()
    mock_filter.exists.return_value = True
    with patch(
        "locations.utils.helpers.Country.objects.filter", return_value=mock_filter
    ):
        # Test with a valid country code
        invalid_code = await validate_country_code("US")
        assert invalid_code is None

        # Test with a valid country name
        valid_country_name = "United States"
        invalid_name = await validate_country_code(valid_country_name)
        assert invalid_name is None

    # Mock Country.objects.filter to return False for exists()
    mock_filter.exists.return_value = False
    with patch(
        "locations.utils.helpers.Country.objects.filter", return_value=mock_filter
    ):
        # Test with an invalid country code
        invalid_country_code = "WÙ"
        response = await validate_country_code(invalid_country_code)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 400
        assert response.content.decode() == "Invalid country code."

        # Test with an invalid country name
        invalid_country_name = "InvalidCountry"
        response = await validate_country_code(invalid_country_name)
        assert isinstance(response, HttpResponse)
        assert response.status_code == 400
        assert response.content.decode() == "Invalid country name."
