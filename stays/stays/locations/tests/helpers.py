from httpx import Response as httpx_response
from locations.tests.datasets import INVALID_COUNTRY_CODES

# Mock pour httpx.AsyncClient
class MockClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def get(self, url, headers=None):
        if any(code in url for code in INVALID_COUNTRY_CODES):
            return httpx_response(400, json={})
        else:
            return httpx_response(200, json={'data': 'country_data'})

# Mock pour cache
class MockCache:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value