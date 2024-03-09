import random
from datetime import datetime
from unittest import mock
from unittest.mock import patch
from uuid import uuid4

import pytest
from cities_light.models import Country
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from model_bakery import baker

# User = get_user_model()
from core.models import Publication
from core.utils.models_helpers import ContentTypes
from core.views import PublicationDetailView
from stays.utils.common_helpers import uuid_generator
from users.models import Profile


@pytest.mark.django_db
class TestPublicationDetailView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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

        # Création d'une instance de Country
        self.country = Country.objects.create(name="France", code2="FR")
        self.words = [
            "Full",
            "Story",
            "Test",
            "Publication",
            "Voice",
            "Audio",
            "Home",
            "View" "apple",
            "banana",
            "cherry",
            "date",
            "elderberry",
            "fig",
            "grape",
            "honeydew",
            "iceberg",
            "jackfruit",
            "kiwi",
            "lemon",
            "mango",
            "nectarine",
            "orange",
            "pineapple",
            "quince",
            "raspberry",
            "strawberry",
            "tangerine",
            "ugli",
            "vanilla",
            "watermelon",
            "xigua",
            "yellow",
        ]
        # Création de plusieurs instances de Publication

        Publication.objects.create(
            uuid=uuid4(),
            title=" ".join(random.choices(self.words, k=5)),
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
        self.publication = Publication.objects.all().first()
        # Création d'un client de test
        self.client = Client(enforce_csrf_checks=False)
        self.url = reverse("core:edit_publication", args=[self.publication.uuid])
        # Create a request object
        self.request = HttpRequest()
        self.request.method = "GET"
        # self.client.force_login(self.profile)  # Log in the user

    @patch("core.views.get_object_or_404")
    @patch("core.views.get_author_picture_from_slug")
    @patch("core.views.find_cities_light_country_name_with_code")
    @patch("core.views.find_cities_light_continent_with_country_code")
    @patch("core.views.get_continent_from_code")
    @patch("core.views.PublicationUpvote.objects.filter")
    @patch("core.models.Publication")
    @patch("users.signals.update_user_status")
    def test_get_object_and_context_data(
        self,
        mock_update_user_status,
        mock_publication,
        mock_filter,
        mock_get_continent_from_code,
        mock_find_cities_light_continent_with_country_code,
        mock_find_cities_light_country_name_with_code,
        mock_get_author_picture_from_slug,
        mock_get_object_or_404,
    ):
        # Création d'une instance de la vue1
        view = PublicationDetailView()
        view.kwargs = {"uuid": "123"}

        # Simulation des méthodes
        mock_get_object_or_404.return_value = mock.Mock(
            author_slug="author",
            country_code_of_stay="US",
            published_from_country_code="US",
        )
        mock_get_author_picture_from_slug.return_value = "picture.jpg"
        mock_find_cities_light_country_name_with_code.return_value = "United States"
        mock_find_cities_light_continent_with_country_code.return_value = "NA"
        mock_get_continent_from_code.return_value = "North America"
        mock_filter.return_value.exists.return_value = False
        mock_filter.return_value.count.return_value = 10

        # Création d'une requête factice
        request = self.factory.get("/fake-url/")
        request.user = AnonymousUser()
        view.request = request

        # Appel de la méthode get_object
        publication = view.get_object()

        # Vérification de l'objet retourné
        self.assertEqual(publication.author_profile_picture, "picture.jpg")
        self.assertEqual(publication.stay_country_name, "United States")
        self.assertEqual(publication.stay_continent_code, "North America")
        self.assertEqual(publication.published_from_country_name, "United States")

        # Appel de la méthode get_context_data
        context = view.get_context_data(object=publication)

        # Vérification du contexte
        self.assertFalse(context["has_upvoted"])
        self.assertEqual(context["publication"].total_upvotes_count, 10)
