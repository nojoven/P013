import pytest
from django.core.cache import cache

from locations.tests.helpers import MockCache, MockClient


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def mock_client(mocker):
    mocker.patch("httpx.AsyncClient", return_value=MockClient())


@pytest.fixture
def mock_cache(mocker):
    mocker.patch("django.core.cache.cache", new_callable=MockCache)
