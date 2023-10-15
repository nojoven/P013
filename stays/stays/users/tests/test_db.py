from django.test import TestCase
from ..models import Profile, ProfileFollowers, ProfileHasDetectedData


# Create your tests here.

def test_can_select_all_users():
    profiles = Profile.objects.all().filter(is_superuser=False)
    assert profiles is not None


def test_can_select_all_followers():
    profiles = ProfileFollowers.objects.all()
    assert profiles is not None


def test_can_query_ProfileHasDetectedData():
    profiles = ProfileHasDetectedData.objects.all()
    assert profiles is not None
