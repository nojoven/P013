import pytest
from django.core.cache import cache
from locations.tests.helpers import FakeResponse
from locations.utils.helpers import fetch_additional_data
from locations.tests.fixtures.fixtures import clear_cache, mock_cache  # noqa F401
from locations.tests.datasets import VALID_CAPITALS, HEADERS
from random import choice as rce

# Constantes pour les tests
CAPITAL = rce(VALID_CAPITALS)


@pytest.mark.asyncio
async def test_fetch_additional_data_cache_miss(mocker):
    # Configure le mock pour simuler une réponse HTTP
    async def async_mock(*args, **kwargs):
        return FakeResponse(200, [{"data": "additional_data"}])

    mocker.patch("httpx.AsyncClient.get", new=async_mock)

    # Définit la valeur de cache_key à None dans le vrai cache
    cache_key = f"additional_data_{CAPITAL}"
    cache.set(cache_key, None)

    # Appel à la fonction avec des données de test
    responses = await fetch_additional_data(CAPITAL, HEADERS)

    # Vérifie que les réponses ne sont pas None
    assert responses is not None

    # Vérifie que toutes les réponses ont un code de statut 200
    assert all(response.status_code == 200 for response in responses)
    assert all(isinstance(response._json_data, list) for response in responses)
    for response in responses:
        assert len(response._json_data) > 0
        assert isinstance(response._json_data[0], dict)
        assert len(response._json_data[0]) > 0
        assert all(isinstance(key, str) for key in response._json_data[0].keys())

    # Vérifie que les réponses sont stockées dans le cache
    assert cache.get(cache_key) is not None


@pytest.mark.asyncio
async def test_fetch_additional_data_cache_hit(mocker):
    # Configure le mock pour simuler une réponse HTTP
    async def async_mock(*args, **kwargs):
        return FakeResponse(200, {"data": "additional_data"})

    mocker.patch("httpx.AsyncClient.get", new=async_mock)

    # Configure le mock pour simuler le cache
    mock_cache = mocker.patch("django.core.cache.cache")
    mock_cache.get.return_value = [
        FakeResponse(200, {"data": "additional_data"})
    ] * 3  # Simule des données déjà présentes dans le cache

    # Appel à la fonction avec des données de test
    responses = await fetch_additional_data(CAPITAL, HEADERS)

    # Vérifie que les réponses ne sont pas None
    assert responses is not None

    # Vérifie que toutes les réponses ont un code de statut 200
    assert all(response.status_code == 200 for response in responses)

    # Vérifie que les réponses ne sont pas stockées dans le cache
    mock_cache.set.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_additional_data_invalid_parameters():
    # Teste avec un capital non-string
    with pytest.raises(TypeError):
        await fetch_additional_data(123, HEADERS)

    # Teste avec un capital vide
    with pytest.raises(ValueError):
        await fetch_additional_data("", HEADERS)

    # Teste avec des headers non-dict
    with pytest.raises(TypeError):
        await fetch_additional_data(CAPITAL, "not a dict")

    # Teste avec des headers None
    with pytest.raises(ValueError):
        await fetch_additional_data(CAPITAL, None)


@pytest.mark.asyncio
async def test_fetch_additional_data_api_error(mocker):
    # Configure le mock pour simuler une réponse HTTP avec une erreur
    async def async_mock(*args, **kwargs):
        return FakeResponse(500, {"error": "Internal server error"})

    mocker.patch("httpx.AsyncClient.get", new=async_mock)

    # Appel à la fonction avec des données de test
    with pytest.raises(Exception):
        await fetch_additional_data(CAPITAL, HEADERS)
