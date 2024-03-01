import httpx
import pytest
from django.http import HttpResponse
from locations.utils.helpers import send_http_requests



@pytest.mark.asyncio
async def test_send_http_requests_valid_code():
    # Test with a valid country code
    valid_country_code = "US"
    response = await send_http_requests(valid_country_code)
    assert response is not None
    assert isinstance(response, dict)
    assert "country_details" in response
    assert "country_details_ninjas" in response
    assert response["country_details"][0] is not None
    assert len(response["country_details_ninjas"][0])

@pytest.mark.asyncio
async def test_send_http_requests_invalid_code():
    # Test with an invalid country code
    invalid_country_code = "xx"
    response = await send_http_requests(invalid_country_code)
    assert response is not None
    assert response.status_code == 400
    assert response.content.decode() == "Invalid country code."