import pytest
import logging
from django.test import TestCase
from core import views as core_views
from core.models import PublicationType, Publication, PublicationHasLocation, PublicationHasProfiles


# pytestmark = pytest.mark.django_db

# Create your tests here.

# @pytest.mark.django_db
# class TestCoreViews(TestCase):
#     pass

def test_can_select_all_publication_types_class():
    publications_types = PublicationType.objects.all()
    assert publications_types is not None

def test_can_select_all_publications_class():
    publications = Publication.objects.all()
    assert publications is not None

def test_can_select_all_publication_spots_class():
    publication_spots = PublicationHasLocation.objects.all()
    assert publication_spots is not None

def test_can_select_all_publication_profiles_class():
    likers = PublicationHasProfiles.objects.all()
    assert likers is not None


