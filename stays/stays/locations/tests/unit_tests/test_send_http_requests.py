import pytest
from unittest.mock import patch, AsyncMock
from locations.utils.helpers import send_http_requests
from icecream import ic
from unittest.mock import MagicMock

# Mock responses for fetch_country_data
mock_response_valid = MagicMock()
mock_response_valid.status_code = 200
mock_response_valid.json.return_value = {"data": "country_data"}

mock_response_invalid = MagicMock()
mock_response_invalid.status_code = 400
mock_response_invalid.json.return_value = {"data": "country_data"}


@patch("locations.utils.helpers.fetch_country_data", new_callable=AsyncMock, return_value=[mock_response_valid, mock_response_valid])
@pytest.mark.asyncio
async def test_send_http_requests_valid_code(mock_fetch_country_data):
    # Test with a valid country code
    valid_country_code = "US"
    response = await send_http_requests(valid_country_code)
    assert response is not None
    assert response["country_details"] == {"data": "country_data"}
    assert response["country_details_ninjas"] == {"data": "country_data"}

@patch("locations.utils.helpers.fetch_country_data", new_callable=AsyncMock, return_value=[mock_response_invalid, mock_response_invalid])
@pytest.mark.asyncio
async def test_send_http_requests_invalid_code(mock_fetch_country_data):
    # Test with an invalid country code
    invalid_country_code = "WÙ"
    response = await send_http_requests(invalid_country_code)
    assert response is not None
    assert response.status_code == 400
    assert response.content.decode() == "Invalid country code."