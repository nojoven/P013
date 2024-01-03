from django.test import TestCase
from ..models import Profile


# Create your tests here.

def test_can_select_all_users():
    profiles = Profile.objects.all().filter(is_superuser=False)
    assert profiles is not None
