import pytest
from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker
from core.models import Publication
from cities_light.models import Country
from stays.utils.common_helpers import uuid_generator
from users.models import Profile
from core.utils.models_helpers import ContentTypes
from uuid import uuid4
from datetime import datetime
import random
from icecream import ic


@pytest.mark.django_db
class TestHomeView(TestCase):
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
        for need in range(12):
            Publication.objects.create(
                uuid=uuid4(),
                title=" ".join(random.choices(self.words, k=3)),
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
        self.publications = Publication.objects.all()
        # Création d'un client de test
        self.client = Client(enforce_csrf_checks=False)
        self.url = reverse("core:home")

    def test_home_view(self):
        session = self.client.session
        session["force_renew_session"] = True
        session.save()

        # Test avec page=1
        response = self.client.get(f"{self.url}?page=1")
        assert response.status_code == 200
        assert "page_obj" in response.context
        assert len(response.context["page_obj"]) == 5  # Vérification de la pagination
        assert isinstance(response.context["page_obj"][0], Publication)
        assert isinstance(response.context["page_obj"][0].title, str)
        assert response.context["page_obj"][0].title in self.publications.values_list(
            "title", flat=True
        )

    def test_home_view_page_2(self):
        session = self.client.session
        session["force_renew_session"] = True
        session.save()

        # Test avec page=2
        response = self.client.get(f"{self.url}?page=2")
        assert response.status_code == 200
        assert "page_obj" in response.context
        assert len(response.context["page_obj"]) == 5  # Vérification de la pagination
        assert isinstance(response.context["page_obj"][0], Publication)
        assert isinstance(response.context["page_obj"][0].title, str)
        assert response.context["page_obj"][0].title in self.publications.values_list(
            "title", flat=True
        )

    def test_home_view_page_3(self):
        session = self.client.session
        session["force_renew_session"] = True
        session.save()

        # Test avec page supérieure au nombre total de pages
        response = self.client.get(f"{self.url}?page=3")
        assert response.status_code == 200
        assert "page_obj" in response.context
        assert (
            len(response.context["page_obj"]) == 2
        )  # Pas de publications sur cette page

    def test_too_big_page_number(self):
        # Check that the session variable has been reset
        session = self.client.session
        session["force_renew_session"] = True
        session.save()
        # Test avec page supérieure au nombre total de pages
        response = self.client.get(f"{self.url}?page=15")
        assert response.status_code == 200
        ic(response)
        # assert "?page=1" in response.url
        self.assertTemplateUsed(response, "feed.html")

    def test_home_view_with_no_page_query_param(self):
        # Check that the session variable has been reset
        session = self.client.session
        session["force_renew_session"] = True
        session.save()
        # Test with page=1
        response = self.client.get(f"{self.url}")
        assert response.status_code == 302
        assert "?page=1" in str(response.url)

    def test_home_view_with_invalid_page(self):
        # Check that the session variable has been reset
        session = self.client.session
        session["force_renew_session"] = True
        session.save()
        # Test avec page non numérique
        with self.assertRaises(ValueError):
            response = self.client.get(f"{self.url}?page=abc")
            assert response.status_code == 200
            assert "page_obj" in response.context
            assert len(response.context["page_obj"]) == 5  # Retour à la première page
            assert response.context["page_obj"][0] == self.publications[0]
            self.assertTemplateUsed(response, "feed.html")
            # Check that the Cache-Control header is set correctly
            self.assertEqual(
                response["Cache-Control"],
                "no-cache, no-store, must-revalidate, private",
            )
            self.assertFalse(session["force_renew_session"])
