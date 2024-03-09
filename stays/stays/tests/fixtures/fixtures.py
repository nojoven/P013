import pytest
from django.test import Client
from django.utils.text import slugify

from stays.utils.common_helpers import uuid_generator
from users.models import Profile


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def profile_online(db):
    # Create a test profile
    profile = Profile.objects.create(
        email="test@example.com",
        password="testpassword",
        username="testuser",
        is_online=True,
        slug=slugify(f"{'test@example.com'.split('@')[0]}{uuid_generator()}"),
    )
    profile.save()
    return profile


@pytest.fixture
def profile_offline(db):
    # Create a test profile
    profile = Profile.objects.create(
        email="test@example.com",
        password="testpassword",
        username="testuser",
        is_online=False,
        slug=slugify(f"{'test@example.com'.split('@')[0]}{uuid_generator()}"),
    )
    profile.save()
    return profile
