import pytest
from django.urls import reverse
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
        self.profile = baker.make(
            Profile,
            email="testadmin@example.com",
            slug=f"testadmin{uuid_generator()}",
            username="testadmin",
            profile_picture="picture.jpg",
        )
        self.profile.set_password("testpasYEF93*&5sword")
        self.profile.save()
        self.client = Client(enforce_csrf_checks=False)

        # Création d'une instance de Country
        self.country = Country.objects.create(name="Italy", code2="IT")

        # Création d'une instance de Publication
        self.voice_publication = baker.make(
            Publication,
            uuid=uuid4(),
            title="Full Story",
            author_username=self.profile.username,
            author_slug=self.profile.slug,
            picture="picture.jpg",
            voice_story="voice.mp3",
            content_type=ContentTypes.voice.value[0],
            season_of_stay="Winter",
            year_of_stay=2000,
            summary="This is a summary.",
            created_at=datetime.now(),
            country_code_of_stay=self.country.code2,
            published_from_country_code="FR",
            upvotes_count=0,
        )
        self.voice_publication.save()

        # Création d'une instance de Publication (text)
        self.text_publication = baker.make(
            Publication,
            uuid=uuid4(),
            title="Full Story",
            author_username=self.profile.username,
            author_slug=self.profile.slug,
            picture="picture.jpg",
            text_story="This is a full story.",
            content_type=ContentTypes.text.value[0],
            season_of_stay="Winter",
            year_of_stay=2000,
            summary="This is a summary.",
            created_at=datetime.now(),
            country_code_of_stay=self.country.code2,
            published_from_country_code="FR",
            upvotes_count=0,
        )
        self.text_publication.save()

    # @patch('django.contrib.auth.mixins.LoginRequiredMixin', new_callable=lambda: object)
    @patch("users.signals.update_user_status")
    def test_check_user_upvoted_publication(self, mock_update_user_status):
        self.client.force_login(self.profile)
        # Create a PublicationUpvote for the publication and user
        baker.make(
            PublicationUpvote,
            publication=self.voice_publication,
            upvote_profile=self.profile.slug,
        )

        # Call the check_user_upvoted_publication view
        response = self.client.get(
            reverse("core:check_user_upvoted", args=[str(self.voice_publication.uuid)])
        )

        # Check that the response indicates that the user has upvoted the publication
        ic(response.json())
        self.assertEqual(response.json(), {"has_upvoted": True})

    @patch("users.signals.update_user_status")
    def test_check_new_user_not_upvoted_publication(self, mock_update_user_status):
        # Create a new profile
        new_profile = baker.make(
            Profile,
            email="newadmin@example.com",
            slug=f"newadmin{uuid_generator()}",
            username="newadmin",
            profile_picture="picture.jpg",
        )
        new_profile.set_password("newpasYEF93*&5sword")
        new_profile.save()

        # Log in as the new user
        self.client.force_login(new_profile)

        # Call the check_user_upvoted_publication view for the text publication
        response = self.client.get(
            reverse("core:check_user_upvoted", args=[str(self.text_publication.uuid)])
        )

        # Check that the response indicates that the user has not upvoted the publication
        ic(response.json())
        self.assertEqual(response.json(), {"has_upvoted": False})
