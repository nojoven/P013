# Importations nécessaires pour les tests
import pytest
from core.utils.models_helpers import (
    get_profile_from_email,
    get_author_picture_from_slug
)
from stays.utils.common_helpers import uuid_generator
from users.models import Profile
from model_bakery import baker


@pytest.mark.django_db
# Test de la fonction get_profile_from_email
def test_get_profile_from_email():
    # Création d'un profil
    profile = baker.make(Profile, 
    email='testadmin@example.com', 
    slug = f"'testadmin@example.com'{uuid_generator()}",
    username = 'testadmin',
    profile_picture = 'picture.jpg'
    )
    profile.set_password('testpasYEF93*&5sword')
    profile.save()

    # Vérification que get_profile_from_email renvoie le bon profil
    assert get_profile_from_email('testadmin@example.com', Profile) == profile

# Test de la fonction get_author_picture_from_slug
@pytest.mark.django_db
def test_get_author_picture_from_slug():
    
    # Création d'un profil
    profile = baker.make(Profile, 
    email='testadmin@example.com', 
    slug = f"'testadmin@example.com'{uuid_generator()}",
    username = 'testadmin',
    profile_picture = 'picture.jpg'
    )
    profile.set_password('testpasYEF93*&5sword')
    profile.save()

    # Vérification que get_author_picture_from_slug renvoie la bonne image
    assert get_author_picture_from_slug(profile.slug, Profile) == 'picture.jpg'