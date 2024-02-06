import pytest
from django.test import RequestFactory, Client
from users.models import Profile
from users.utils import uuid_generator
from django.utils.text import slugify

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def profile(db):
    # Create a test profile
    profile = Profile.objects.create(
        email='test@example.com',
        password='testpassword',
        is_online=True,
        slug=slugify(f"{'test@example.com'.split('@')[0]}{uuid_generator()}")
    )
    profile.save()
    # yield profile
    # Cleanup after test
    
    print(profile.pk)
    return profile

def test_is_profile_online(client, profile):
    # Make a GET request to the is_profile_online endpoint
    # profile.slug = slugify(f"{profile.email.split('@')[0]}{profile.uuid}")
    # profile.save()
    response = client.get(f'/api/isonline/{profile.slug}/')

    # Check that the response has a status code of 200
    assert response.status_code == 200

    # Check that the response data is correct
    assert response.json() == {'is_online': True}

    # Check that the profile has been deleted
    with pytest.raises(Profile.DoesNotExist):
        Profile.objects.get(slug=profile.slug)
    
    profile.delete()