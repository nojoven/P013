import pytest
from unittest.mock import AsyncMock, patch
from locations.views import fetch_country_data, napk
import httpx
from locations.views import cache
from asgiref.sync import async_to_sync
# Constants for test cases
VALID_COUNTRY_CODES = ['US', 'FR', 'JP']
INVALID_COUNTRY_CODES = ['', 'ZZZ', '123']
HEADERS = {'x-api-key': napk}

async def mock_get(*args, **kwargs):
    return [httpx.Response(200, json={'data': 'country_data'})]




@pytest.mark.asyncio
@pytest.mark.parametrize("country_code, headers, expected_id", [
    # Happy path tests with various realistic test values
    ('US', HEADERS, 'happy_path_us'),
    ('FR', HEADERS, 'happy_path_fr'),
    ('JP', HEADERS, 'happy_path_jp'),
    
    # Edge cases
    ('GB', HEADERS, 'edge_case_gb'),  # Great Britain, common edge case due to different codes (GB, UK)
    
    # Error cases
    ('', HEADERS, 'error_case_empty_code'),  # Empty country code
    ('ZZZ', HEADERS, 'error_case_invalid_code'),  # Invalid country code
    ('123', HEADERS, 'error_case_numeric_code'),  # Numeric country code
])
def test_fetch_country_data(country_code, headers, expected_id, monkeypatch):
    # Arrange
    # Mocking the cache and httpx client
    monkeypatch.setattr('locations.views.cache.get', AsyncMock(return_value='caced_data'))
    monkeypatch.setattr('locations.views.cache.set', AsyncMock())
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[
    mock_get(),
    mock_get()
    ])
    monkeypatch.setattr('httpx.AsyncClient', AsyncMock(return_value=mock_client))

    # Act
    responses = async_to_sync(fetch_country_data)(country_code, headers)

    # Assert
    # Check that the responses are what we expect
    @pytest.mark.asyncio
    assert isinstance(responses, list), f"Test ID: {expected_id} - The response should be a list"
    assert len(responses) == 2, f"Test ID: {expected_id} - There should be two responses"
    assert all(isinstance(response, httpx.Response) for response in responses), f"Test ID: {expected_id} - All items in responses should be httpx.Response instances"
    assert all(response.status_code == 200 for response in responses), f"Test ID: {expected_id} - All responses should have a status code of 200"

    # Check that the cache is being used correctly
    cache.get.assert_awaited_once_with(f'country_data_{country_code}')
    cache.set.assert_awaited_once_with(f'country_data_{country_code}', responses)

    # Check for error cases
    if country_code in INVALID_COUNTRY_CODES:
        assert all(response.status_code == 404 for response in responses), f"Test ID: {expected_id} - Responses should have a status code of 404 for invalid country codes"
