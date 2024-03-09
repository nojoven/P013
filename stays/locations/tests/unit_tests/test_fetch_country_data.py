import pytest

from locations.utils.helpers import fetch_country_data
from locations.tests.datasets import VALID_COUNTRY_CODES, INVALID_COUNTRY_CODES, HEADERS
from locations.tests.fixtures.fixtures import mock_client, mock_cache, clear_cache  # noqa F401
from icecream import ic


# Tests unitaires
@pytest.mark.asyncio
async def test_fetch_country_data_valid_code(mock_client, mock_cache, clear_cache):
    for country_code in VALID_COUNTRY_CODES:
        responses = await fetch_country_data(country_code, HEADERS)
        assert responses is not None
        assert all(response.status_code == 200 for response in responses)
        assert all(
            response.json() == {"data": "country_data"} for response in responses
        )


@pytest.mark.asyncio
async def test_fetch_country_data_invalid_code(mock_client, mock_cache, clear_cache):
    for country_code in INVALID_COUNTRY_CODES:
        ic(country_code)
        responses = await fetch_country_data(country_code, HEADERS)
        assert responses[0].status_code == 400
        assert responses[1].status_code == 400


@pytest.mark.asyncio
async def test_fetch_country_data_missing_headers():
    for country_code in VALID_COUNTRY_CODES:
        with pytest.raises(TypeError):
            await fetch_country_data(country_code)


@pytest.mark.asyncio
async def test_fetch_country_data_none_country_code(mock_client, mock_cache):
    country_code = None
    with pytest.raises(ValueError, match="The country_code parameter cannot be None."):
        await fetch_country_data(country_code, HEADERS)


@pytest.mark.asyncio
async def test_fetch_country_data_empty_country_code(mock_client, mock_cache):
    country_code = ""
    with pytest.raises(ValueError, match="The country_code parameter cannot be empty."):
        await fetch_country_data(country_code, HEADERS)


@pytest.mark.asyncio
async def test_fetch_country_data_none_headers(mock_client, mock_cache):
    country_code = VALID_COUNTRY_CODES[0]
    headers = None
    with pytest.raises(ValueError, match="The headers parameter cannot be None."):
        await fetch_country_data(country_code, headers)


@pytest.mark.asyncio
async def test_fetch_country_data_non_dict_headers(mock_client, mock_cache):
    country_code = VALID_COUNTRY_CODES[0]
    headers = "not a dict"
    with pytest.raises(TypeError, match="The headers parameter must be a dictionary."):
        await fetch_country_data(country_code, headers)


@pytest.mark.asyncio
async def test_fetch_country_data_empty_headers(mock_client, mock_cache):
    country_code = VALID_COUNTRY_CODES[0]
    headers = {}
    with pytest.raises(ValueError, match="The headers dictionary cannot be empty."):
        await fetch_country_data(country_code, headers)


@pytest.mark.asyncio
async def test_fetch_country_data_missing_api_key(mock_client, mock_cache):
    country_code = VALID_COUNTRY_CODES[0]
    headers = {"not-api-key": "value"}
    with pytest.raises(
        KeyError, match="The headers dictionary must contain an 'X-Api-Key' key."
    ):
        await fetch_country_data(country_code, headers)


@pytest.mark.asyncio
async def test_fetch_country_data_invalid_api_key(mock_client, mock_cache):
    country_code = VALID_COUNTRY_CODES[0]
    headers = {"X-Api-Key": "invalid"}
    with pytest.raises(
        ValueError,
        match="The 'X-Api-Key' header value does not match the expected value.",
    ):
        await fetch_country_data(country_code, headers)


@pytest.mark.asyncio
async def test_fetch_country_data_short_api_key(mock_client, mock_cache):
    country_code = VALID_COUNTRY_CODES[0]
    headers = {"X-Api-Key": "short"}
    with pytest.raises(ValueError):
        await fetch_country_data(country_code, headers)
