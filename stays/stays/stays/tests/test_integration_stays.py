import pytest
from django.test import RequestFactory, Client
from users.models import Profile
from users.utils import uuid_generator
from django.utils.text import slugify
from icecream import ic
import sys
from unittest.mock import Mock

@pytest.fixture(autouse=True)
def no_faker(monkeypatch):
    monkeypatch.setitem(sys.modules, 'faker', Mock())

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def profile_online(db):
    # Create a test profile
    profile = Profile.objects.create(
        email='test@example.com',
        password='testpassword',
        username='testuser',
        is_online=True,
        slug=slugify(f"{'test@example.com'.split('@')[0]}{uuid_generator()}")
    )
    profile.save()
    # Cleanup after test
    # yield profile
    # profile.delete()
    
    print(profile.pk)
    return profile

def test_is_profile_online(client, profile_online, no_faker):
    # Make a GET request to the is_profile_online endpoint
    # profile.slug = slugify(f"{profile.email.split('@')[0]}{profile.uuid}")
    # profile.save()
    response = client.get(f'/api/isonline/{profile_online.slug}/')

    # Check that the response has a status code of 200
    assert response.status_code == 200

    # Check that the response data is correct
    assert response.json() == {'is_online': True}
    ic(response.json())

    profile_online.is_online = False
    profile_online.save()

    # Make a GET request to the is_profile_online endpoint
    response = client.get(f'/api/isonline/{profile_online.slug}')

    ic(response)
    # Check that the response has a status code of 200
    assert response.status_code == 200

    ic(profile_online.is_online)
    # Check that the response data is correct
    # assert response.json() == {'is_online': False}

    
    # # Check that the profile has been deleted
    # with pytest.raises(Profile.DoesNotExist):
    #     Profile.objects.get(slug=profile.slug)

# def test_is_profile_offline(client, profile_online):
#     # Get the profile
#     profile_slug = Profile.objects.get(username=profile_online.username).slug
#     profile_online.is_online = False
#     profile_online.save()

#     # Make a GET request to the is_profile_online endpoint
#     response = client.get(f'/api/isonline/{profile_slug}')
#     # Check that the response has a status code of 200
#     assert response.status_code == 200

#     # Check that the response data is correct
#     assert response.json() == {'is_online': False}
