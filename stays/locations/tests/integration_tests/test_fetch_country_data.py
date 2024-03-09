import pytest
from icecream import ic
from locations.tests.datasets import VALID_COUNTRY_CODES, INVALID_COUNTRY_CODES, HEADERS
from locations.utils.helpers import fetch_country_data


@pytest.mark.asyncio
async def test_fetch_country_data_valid_code():
    for country_code in VALID_COUNTRY_CODES:
        responses = await fetch_country_data(country_code, HEADERS)

        assert responses is not None
        assert len(responses) == 2
        for response in responses:
            assert response.status_code == 200
            assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_fetch_country_data_invalid_code():
    for country_code in INVALID_COUNTRY_CODES:
        ic(country_code)
        responses = await fetch_country_data(country_code, HEADERS)
        assert responses is not None
        assert len(responses) == 2
        assert responses[0].status_code == 404
        assert responses[1].status_code == 200 and responses[1].json() == []


@pytest.mark.asyncio
async def test_fetch_country_data_missing_api_key():
    for country_code in VALID_COUNTRY_CODES:
        try:
            await fetch_country_data(country_code)
        except TypeError as e:
            assert "missing 1 required positional argument: 'headers'" in str(e)
