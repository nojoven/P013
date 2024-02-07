import pytest
from stays.tests.fixtures.fixtures import profile_offline, profile_online, client



def test_is_profile_online(client, profile_online):
    response = client.get(f'/api/isonline/{profile_online.slug}/')

    # Check that the response has a status code of 200
    assert response.status_code == 200

    # Check that the response data is correct
    assert response.json() == {'is_online': True}


def test_is_profile_offline(client, profile_offline):
    response = client.get(f'/api/isonline/{profile_offline.slug}/')

    # Check that the response has a status code of 200
    assert response.status_code == 200

    # Check that the response data is correct
    assert response.json() == {'is_online': False}
