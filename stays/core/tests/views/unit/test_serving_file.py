import pytest
from core.models import Publication
from users.models import Profile
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from stays.utils.common_helpers import uuid_generator
from uuid import uuid4
from datetime import datetime
from core.utils.models_helpers import ContentTypes
from cities_light.models import Country






class ServeFilesTest(TestCase):
    @pytest.mark.django_db
    def setUp(self):
        # Création d'un profil
        self.profile = baker.make(Profile,
        email='testadmin@example.com',
        slug = f"testadmin{uuid_generator()}",
        username = 'testadmin',
        profile_picture = 'picture.jpg'
        )
        self.profile.set_password('testpasYEF93*&5sword')
        self.profile.save()
        self.client = Client(enforce_csrf_checks=False)

        # Création d'une instance de Country
        self.country = Country.objects.create(name='Italy', code2='IT')

        # Création d'une instance de Publication
        self.voice_publication = baker.make(Publication, 
        uuid = uuid4(),
        title='Full Story', 
        author_username=self.profile.username, 
        author_slug=self.profile.slug, 
        picture=SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),
        voice_story=SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg"),
        content_type=ContentTypes.voice.value[0],
        season_of_stay='Winter',
        year_of_stay=2000,
        summary='This is a summary.',
        created_at=datetime.now(),
        country_code_of_stay=self.country.code2,
        published_from_country_code="FR",
        upvotes_count=0
        )
        self.voice_publication.save()

    
    def test_serve_publication_picture(self):
        # Appel de la vue avec l'UUID de la publication
        picture_response = self.client.get(f'/publications/publication/{self.voice_publication.uuid}/picture')

        # Vérification que la vue renvoie une réponse avec le statut 200
        self.assertEqual(picture_response.status_code, 200)

        # Vérification que le contenu de la réponse est le contenu de l'image
        response_content = b''.join(picture_response.streaming_content)
        self.assertEqual(response_content, b"file_content")

    
    def test_serve_publication_audio(self):
        # Call the view with the UUID of the publication
        voice_response = self.client.get(f'/publications/publication/{self.voice_publication.uuid}/audio')

        # Verify that the view returns a response with status 200
        self.assertEqual(voice_response.status_code, 200)

        # Verify that the content of the response is the content of the audio file
        response_content = b''.join(voice_response.streaming_content)
        self.assertEqual(response_content, b"file_content")