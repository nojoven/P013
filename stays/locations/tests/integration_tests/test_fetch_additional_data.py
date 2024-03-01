from random import choice as rce
import pytest
from icecream import ic
# from unittest.mock import AsyncMock, patch
from locations.tests.datasets import HEADERS, VALID_CAPITALS, INVALID_CAPITALS
from locations.utils.helpers import fetch_additional_data
from locations.tests.fixtures.fixtures import clear_cache # noqa F401
from django.core.cache import cache
headers = HEADERS


@pytest.mark.asyncio
async def test_valid_capital():

    capital = rce(VALID_CAPITALS)

    # Appel à la fonction avec des données de test
    responses = await fetch_additional_data(capital, HEADERS)

    # Vérifie que les réponses ne sont pas None
    assert responses is not None
    assert all(response is not None for response in responses)
    assert len(responses) == 3
    ic(f"{capital}")
    ic((response.status_code for response in responses))
    # Vérifie que toutes les réponses ont un code de statut 200
    assert all(response.status_code == 200 for response in responses)

    # Vérifie que les réponses sont stockées dans le cache
    cache_key = f"additional_data_{capital}"
    cached_responses = cache.get(cache_key)
    assert cached_responses is not None

    # Compare les codes de statut et les corps des réponses
    assert [response.status_code for response in cached_responses] == [response.status_code for response in responses]
    assert [response.json() for response in cached_responses] == [response.json() for response in responses]

    cache.clear()
    assert cache.get(cache_key) is None

@pytest.mark.asyncio
async def test_wrong_capital():

    capital = rce(INVALID_CAPITALS)

     # Appel à la fonction avec des données de test
    with pytest.raises(Exception) as excinfo:
        await fetch_additional_data(capital, HEADERS)

    assert "API request failed with status code 400" in str(excinfo.value)


@pytest.mark.asyncio
async def test_headers_are_missing():

    capital = rce(INVALID_CAPITALS)

    # Appel à la fonction avec des données de test
    try:
        await fetch_additional_data(capital)
    except TypeError as e:
        assert "missing 1 required positional argument: 'headers'" in str(e)

@pytest.mark.asyncio
async def test_capital_is_missing():

    # Appel à la fonction avec des données de test
    try:
        await fetch_additional_data(HEADERS)
    except TypeError as e:
        assert "missing 1 required positional argument: 'headers'" in str(e)

@pytest.mark.asyncio
async def test_capital_is_none():

    capital = None
    # Appel à la fonction avec des données de test
    with pytest.raises(TypeError):
        await fetch_additional_data(capital, None)

@pytest.mark.asyncio
async def test_headers_is_none():
    capital = rce(VALID_CAPITALS)
    # Appel à la fonction avec des données de test
    with pytest.raises(ValueError):
        await fetch_additional_data(capital, None)


@pytest.mark.asyncio
async def test_empty_headers():
    capital = rce(VALID_CAPITALS)
    # Appel à la fonction avec des données de test
    with pytest.raises(ValueError):
        await fetch_additional_data(capital, {})


@pytest.mark.asyncio
async def test_wrong_capital_type():
    capital = 123456
    # Appel à la fonction avec des données de test
    with pytest.raises(TypeError):
        await fetch_additional_data(capital, HEADERS)


@pytest.mark.asyncio
async def test_wrong_headers_type():
    capital = rce(VALID_CAPITALS)
    # Appel à la fonction avec des données de test
    with pytest.raises(TypeError):
        await fetch_additional_data(capital, "HEADERS")
