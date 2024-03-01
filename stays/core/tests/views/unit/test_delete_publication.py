import pytest
from django.test import TestCase, Client
from django_webtest import WebTest
from model_bakery import baker
from stays.utils.common_helpers import uuid_generator
from datetime import datetime
from cities_light.models import Country
from core.models import Publication, PublicationUpvote
from users.models import Profile
from core.utils.models_helpers import ContentTypes
from uuid import uuid4
from icecream import ic
from unittest.mock import patch
import json

class TestCheckUserUpvotedPublicationView(WebTest, TestCase):

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
        picture='picture.jpg', 
        voice_story='voice.mp3',
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

        # Création d'une instance de Publication (text)
        self.text_publication = baker.make(Publication,
        uuid = uuid4(),
        title='Full Story', 
        author_username=self.profile.username, 
        author_slug=self.profile.slug, 
        picture='picture.jpg',
        text_story='This is a full story.',
        content_type=ContentTypes.text.value[0],
        season_of_stay='Winter',
        year_of_stay=2000,
        summary='This is a summary.',
        created_at=datetime.now(),
        country_code_of_stay=self.country.code2,
        published_from_country_code="FR",
        upvotes_count=0
        )
        self.text_publication.save()

    # @patch('django.contrib.auth.mixins.LoginRequiredMixin', new_callable=lambda: object)

 
    @patch('users.signals.update_user_status')
    def test_delete_publication(self, mock_update_user_status):
        
        self.assertTrue(Publication.objects.filter(
            uuid=self.voice_publication.uuid
        ).exists())
       
        self.client.force_login(self.profile)
        
        self.voice_publication.refresh_from_db()

        response = self.client.post(
            '/publications/publication/rm',
            data=json.dumps({	
                'identifier': str(self.voice_publication.uuid)
            }),
            content_type='application/json'
        )

        # Vérification que la réponse a un statut de succès
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})

        self.assertFalse(Publication.objects.filter(
            uuid=self.voice_publication.uuid
        ).exists())