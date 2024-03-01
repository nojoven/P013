import pytest
from django.test import Client
from users.models import Profile
from stays.utils.common_helpers import uuid_generator
from django.utils.text import slugify
# import sys
# from unittest.mock import Mock


# @pytest.fixture(autouse=True)
# def no_faker(monkeypatch):
#     monkeypatch.setitem(sys.modules, 'faker', Mock())

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
    return profile

@pytest.fixture
def profile_offline(db):
    # Create a test profile
    profile = Profile.objects.create(
        email='test@example.com',
        password='testpassword',
        username='testuser',
        is_online=False,
        slug=slugify(f"{'test@example.com'.split('@')[0]}{uuid_generator()}")
    )
    profile.save()
    return profile