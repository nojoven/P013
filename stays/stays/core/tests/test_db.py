from django.test import TestCase
from ..models import PublicationType, Publication, PublicationHasLocation, PublicationHasProfiles

# Create your tests here.

def test_can_select_all_publication_types():
    publications_types = PublicationType.objects.all()
    assert publications_types is not None

def test_can_select_all_publications():
    publications = Publication.objects.all()
    assert publications is not None

def test_can_select_all_publication_spots():
    publication_spots = PublicationHasLocation.objects.all()
    assert publication_spots is not None

def test_can_select_all_publication_profiles():
    likers = PublicationHasProfiles.objects.all()
    assert likers is not None
