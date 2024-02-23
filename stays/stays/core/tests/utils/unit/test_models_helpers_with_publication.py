import pytest
from datetime import datetime
from model_bakery import baker
from core.models import Publication
from users.models import Profile
from core.utils.models_helpers import voice_story_upload_to, picture_upload_to
from stays.utils.common_helpers import uuid_generator
from django.urls import reverse

@pytest.mark.django_db
def test_publication_instance_model_helpers():
    # Création d'un profil
    profile = baker.make(Profile,
    email='testadmin@example.com',
    slug = f"'testadmin@example.com'{uuid_generator()}",
    username = 'testadmin',
    profile_picture = 'picture.jpg'
    )
    profile.set_password('testpasYEF93*&5sword')
    profile.save()

    # Création d'une instance de Publication
    publication = baker.make(Publication, title='Title One', author_username=profile.username, author_slug=profile.slug, picture='picture.jpg', voice_story='voice.mp3')

    # Vérification que voice_story_upload_to renvoie le bon chemin
    assert voice_story_upload_to(publication, 'voice.mp3') == f'uploads/{publication.author_slug}/{datetime.now().strftime("%Y/%m/%d")}/{publication.uuid}/voice/voice.mp3'

    # Vérification que picture_upload_to renvoie le bon chemin
    assert picture_upload_to(publication, 'picture.jpg') == f'uploads/{publication.author_slug}/{datetime.now().strftime("%Y/%m/%d")}/{publication.uuid}/picture/picture.jpg'

    # Vérification de la méthode __str__
    assert str(publication) == 'Title One'

    # Vérification de la méthode get_absolute_url
    assert publication.get_absolute_url() == reverse('users:account', args=[publication.author_slug])
