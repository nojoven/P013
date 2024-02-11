import pytest
from locations.utils.helpers import fetch_additional_data  # Remplacez par le chemin d'accès correct à votre fonction

# Constantes pour les tests
CAPITAL = 'Paris'
HEADERS = {'X-Api-Key': 'your_api_key'}

@pytest.mark.asyncio
async def test_fetch_additional_data(mocker):
    # Configure le mock pour simuler une réponse HTTP
    mock_get = mocker.patch('httpx.AsyncClient.get', new_callable=pytest.AsyncMock)
    mock_get.return_value = pytest.AsyncMock(status_code=200, json=pytest.AsyncMock(return_value={'data': 'additional_data'}))

    # Configure le mock pour simuler le cache
    mock_cache = mocker.patch('your_module.cache')  # Remplacez par le chemin d'accès correct à votre cache
    mock_cache.get.return_value = None

    # Appel à la fonction avec des données de test
    responses = await fetch_additional_data(CAPITAL, HEADERS)

    # Vérifie que les réponses ne sont pas None
    assert responses is not None

    # Vérifie que toutes les réponses ont un code de statut 200
    assert all(response.status_code == 200 for response in responses)

    # Vérifie que les réponses sont stockées dans le cache
    mock_cache.set.assert_called_once()

@pytest.mark.asyncio
async def test_fetch_additional_data_invalid_parameters():
    # Teste avec un capital non-string
    with pytest.raises(TypeError):
        await fetch_additional_data(123, HEADERS)

    # Teste avec un capital vide
    with pytest.raises(ValueError):
        await fetch_additional_data('', HEADERS)

    # Teste avec des headers non-dict
    with pytest.raises(TypeError):
        await fetch_additional_data(CAPITAL, 'not a dict')

    # Teste avec des headers None
    with pytest.raises(ValueError):
        await fetch_additional_data(CAPITAL, None)