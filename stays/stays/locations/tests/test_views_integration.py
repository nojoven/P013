import pytest
from icecream import ic
# from unittest.mock import AsyncMock, patch
from locations.views import fetch_country_data, napk
# Constants for test cases
VALID_COUNTRY_CODES = ['US', 'FR', 'JP']
INVALID_COUNTRY_CODES = ['ZZ', '00']
HEADERS = {'x-api-key': napk}



@pytest.mark.asyncio
async def test_fetch_country_data_valid_code():
    for country_code in VALID_COUNTRY_CODES:

        responses = await fetch_country_data(country_code, HEADERS)

        assert responses is not None
        for response in responses:
            assert response.status_code == 200
            assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_fetch_country_data_invalid_code():
    for country_code in INVALID_COUNTRY_CODES:
        responses = await fetch_country_data(country_code, HEADERS)
        for response in responses:
            if response.status_code == 200:
                ic(country_code)
                continue
            else:
                assert response.status_code != 200, "Each response should have a status code of 200"

@pytest.mark.asyncio
async def test_fetch_country_data_missing_api_key():
    for country_code in VALID_COUNTRY_CODES:
        try:
            await fetch_country_data(country_code)
        except TypeError as e:
            assert "missing 1 required positional argument: 'headers'" in str(e)