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
    def test_upvote(self, mock_update_user_status):
        self.assertFalse(PublicationUpvote.objects.filter(
            publication=self.voice_publication,
            upvote_profile=self.profile.slug
        ).exists())
        self.assertEqual(self.voice_publication.upvotes_count, 0)
        self.client.force_login(self.profile)
        self.voice_publication.upvotes_count = 0
        self.voice_publication.save()
        self.voice_publication.refresh_from_db()
        response = self.client.post(
            f'/publications/publication/{self.voice_publication.uuid}/upvote',
            data={
                'uuid': str(self.voice_publication.uuid),
                'profile_email': self.profile.email,
            }
        )
        ic(type(response))
        self.assertEqual(response.status_code, 200)
        self.assertIn("You Like It", response.content.decode())
        self.assertNotIn(">Upvote<", response.content.decode())


        upvote = PublicationUpvote.objects.get(
            publication=self.voice_publication,
            upvote_profile=self.profile.slug
        )
        self.assertIsNotNone(upvote)
        self.assertEqual(upvote.upvote_value, 1)

        self.voice_publication.refresh_from_db()
        self.assertGreater(self.voice_publication.upvotes_count, 0)
        self.assertEqual(self.voice_publication.upvotes_count, 1)



    @patch('users.signals.update_user_status')
    def test_unvote(self, mock_update_user_status):
        new_vote = baker.make(PublicationUpvote,
        publication=self.text_publication,
        upvote_profile=self.profile.slug,
        upvote_value=1
        )
        new_vote.save()
        # PublicationUpvote.objects.create(
        #     publication=self.text_publication,
        #     upvote_profile=self.profile.slug
        # )
        self.text_publication.upvotes_count = 1
        self.text_publication.save()
        self.text_publication.refresh_from_db()

        self.client.force_login(self.profile)
        response = self.client.post(
            f'/publications/publication/{self.text_publication.uuid}/upvote',
            data={
                'uuid': str(self.text_publication.uuid),
                'profile_email': self.profile.email,
            }
        )
        ic(type(response))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("You Like It", response.content.decode())
        self.assertIn(">Upvote<", response.content.decode())

        ic(PublicationUpvote.objects.all())

        self.assertFalse(PublicationUpvote.objects.filter(
            publication=self.text_publication,
            upvote_profile=self.profile.slug
        ).exists())
    
        self.text_publication.refresh_from_db()
        self.assertEqual(self.text_publication.upvotes_count, 0)

