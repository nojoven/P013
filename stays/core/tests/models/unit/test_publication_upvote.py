# Importations nécessaires pour les tests
from datetime import datetime

from django.test import TestCase
from model_bakery import baker

from core.models import Publication, PublicationUpvote
from core.utils.models_helpers import ContentTypes
from stays.utils.common_helpers import uuid_generator
from users.models import Profile


class PublicationUpvoteModelTest(TestCase):
    def setUp(self):
        # Création d'un profil
        self.profile = baker.make(
            Profile,
            email="testadmin@example.com",
            slug=f"testadmin{uuid_generator()}",
            username="testadmin",
            profile_picture="picture.jpg",
        )
        self.profile.set_password("testpasYEF93*&5sword")
        self.profile.save()

        # Création d'un second profil
        self.profile2 = baker.make(
            Profile,
            email="testadmin2@example.com",
            slug=f"testadmin2{uuid_generator()}",
            username="testadmin2",
            profile_picture="picture2.jpg",
        )
        self.profile2.set_password("tes222tpasYEF93ailesword")
        self.profile2.save()

        # Création d'une instance de Publication avec tous les champs remplis
        self.full_publication = baker.make(
            Publication,
            title="Full Story",
            author_username=self.profile.username,
            author_slug=self.profile.slug,
            picture="picture.jpg",
            voice_story="voice.mp3",
            text_story="This is a full story.",
            content_type=ContentTypes.text.value[0],
            season_of_stay="Winter",
            year_of_stay=2000,
            summary="This is a summary.",
            created_at=datetime.now(),
            country_code_of_stay="IT",
            published_from_country_code="FR",
            upvotes_count=0,
        )
        self.full_publication.save()

        self.publication_upvote1 = baker.make(
            PublicationUpvote,
            publication=self.full_publication,
            upvote_profile=self.profile.slug,
            upvote_value=1,
        )
        self.publication_upvote1.save()

    def test_publication_first_upvote(self):
        self.assertEqual(self.publication_upvote1.publication, self.full_publication)
        self.assertEqual(self.publication_upvote1.upvote_profile, self.profile.slug)
        self.assertEqual(len(PublicationUpvote.objects.all()), 1)
        self.assertEqual(self.publication_upvote1.upvote_value, 1)
        self.full_publication.refresh_from_db()
        # 2 because this test does not mute the signals
        self.assertEqual(self.full_publication.upvotes_count, 1)

    def test_publication_second_upvote(self):
        publication_upvote2 = baker.make(
            PublicationUpvote,
            publication=self.full_publication,
            upvote_profile=self.profile2.slug,
            upvote_value=1,
        )
        publication_upvote2.save()

        self.assertEqual(publication_upvote2.publication, self.full_publication)
        self.assertEqual(publication_upvote2.upvote_profile, self.profile2.slug)
        self.assertEqual(len(PublicationUpvote.objects.all()), 2)
        self.assertEqual(publication_upvote2.upvote_value, 1)
        self.full_publication.refresh_from_db()
        # 4 because this test does not mute the signals
        self.assertEqual(self.full_publication.upvotes_count, 2)
