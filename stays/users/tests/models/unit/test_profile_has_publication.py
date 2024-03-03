import pytest
from model_bakery import baker
from users.models import ProfileHasPublication 
from django.db import IntegrityError

from users.models import Profile
from core.models import Publication
from django.contrib.auth.hashers import make_password

from django.db.models.signals import post_save
from core.signals import create_profile_has_publication

@pytest.fixture
def mock_profile():
    # Créez et sauvegardez un objet Profile mock dans la base de données
    password = make_password('test_password')
    return baker.make(Profile, email='test@example.com', password=password)

@pytest.fixture
def mock_publication(mock_profile):
    # Créez et sauvegardez un objet Publication mock dans la base de données
    return baker.make(Publication, author_slug=mock_profile.slug)

@pytest.mark.django_db
def test_profile_has_publication(db, mock_profile, mock_publication):
    # Désactivez le signal create_profile_has_publication
    post_save.disconnect(create_profile_has_publication, sender=Publication)
    # Supprimez tous les objets ProfileHasPublication
    ProfileHasPublication.objects.all().delete()

    # Créez une instance de ProfileHasPublication
    profile_has_publication = baker.make(ProfileHasPublication, user_profile=mock_profile, publication_of_user=mock_publication)
 
    # Vérifiez que les champs sont correctement définis
    assert profile_has_publication.user_profile == mock_profile
    assert profile_has_publication.publication_of_user == mock_publication

    # Vérifiez que la contrainte unique_together fonctionne
    with pytest.raises(IntegrityError):
        baker.make(ProfileHasPublication, user_profile=mock_profile, publication_of_user=mock_publication)

    # Réactivez le signal create_profile_has_publication
    post_save.connect(create_profile_has_publication, sender=Publication)

@pytest.mark.django_db
def test_delete_profile_has_publication(db, mock_profile, mock_publication):
    # Désactivez le signal create_profile_has_publication
    post_save.disconnect(create_profile_has_publication, sender=Publication)
    # Supprimez tous les objets ProfileHasPublication
    ProfileHasPublication.objects.all().delete()

    # Créez une instance de ProfileHasPublication
    profile_has_publication = baker.make(ProfileHasPublication, user_profile=mock_profile, publication_of_user=mock_publication)
 
    # Vérifiez que l'objet existe dans la base de données
    assert ProfileHasPublication.objects.filter(user_profile=mock_profile, publication_of_user=mock_publication).exists()

    # Supprimez l'objet
    profile_has_publication.delete()

    # Vérifiez que l'objet n'existe plus dans la base de données
    assert not ProfileHasPublication.objects.filter(user_profile=mock_profile, publication_of_user=mock_publication).exists()

    # Réactivez le signal create_profile_has_publication
    post_save.connect(create_profile_has_publication, sender=Publication)


@pytest.mark.django_db
def test_delete_profile_deletes_profile_has_publication(db, mock_profile, mock_publication):
    # Désactivez le signal create_profile_has_publication
    post_save.disconnect(create_profile_has_publication, sender=Publication)
    # Supprimez tous les objets ProfileHasPublication
    ProfileHasPublication.objects.all().delete()

    # Créez une instance de ProfileHasPublication
    baker.make(ProfileHasPublication, user_profile=mock_profile, publication_of_user=mock_publication)
 
    # Supprimez le profil
    mock_profile.delete()

    # Vérifiez que l'entrée ProfileHasPublication a été supprimée
    assert not ProfileHasPublication.objects.filter(user_profile=mock_profile, publication_of_user=mock_publication).exists()

    # Réactivez le signal create_profile_has_publication
    post_save.connect(create_profile_has_publication, sender=Publication)

@pytest.mark.django_db
def test_delete_publication_deletes_profile_has_publication(db, mock_profile, mock_publication):
    # Désactivez le signal create_profile_has_publication
    post_save.disconnect(create_profile_has_publication, sender=Publication)
    # Supprimez tous les objets ProfileHasPublication
    ProfileHasPublication.objects.all().delete()

    # Créez une instance de ProfileHasPublication
    baker.make(ProfileHasPublication, user_profile=mock_profile, publication_of_user=mock_publication)
 
    # Supprimez la publication
    mock_publication.delete()

    # Vérifiez que l'entrée ProfileHasPublication a été supprimée
    assert not ProfileHasPublication.objects.filter(user_profile=mock_profile, publication_of_user=mock_publication).exists()

    # Réactivez le signal create_profile_has_publication
    post_save.connect(create_profile_has_publication, sender=Publication)
