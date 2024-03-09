# Importations nécessaires pour les tests
from datetime import datetime
from model_bakery import baker
from core.models import Publication
from users.models import Profile
from stays.utils.common_helpers import uuid_generator
from django.test import TestCase
from django.urls import reverse
from core.utils.models_helpers import ContentTypes


class PublicationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création d'un profil
        cls.profile = baker.make(
            Profile,
            email="testadmin@example.com",
            slug=f"'testadmin@example.com'{uuid_generator()}",
            username="testadmin",
            profile_picture="picture.jpg",
        )
        cls.profile.set_password("testpasYEF93*&5sword")
        cls.profile.save()

        # Création d'une instance de Publication
        cls.publication = baker.make(
            Publication,
            title="Title One",
            author_username=cls.profile.username,
            author_slug=cls.profile.slug,
            picture="picture.jpg",
            voice_story="voice.mp3",
        )

    def test_str(self):
        self.assertEqual(str(self.publication), "Title One")

    def test_get_absolute_url(self):
        expected_url = reverse("users:account", args=[self.publication.author_slug])
        self.assertEqual(self.publication.get_absolute_url(), expected_url)


class PublicationSimpleModelTest(TestCase):
    def test_default_values(self):
        publication = Publication()
        self.assertIsNone(publication.title)
        self.assertIsNone(publication.summary)
        self.assertEqual(publication.year_of_stay, 1990)
        self.assertEqual(publication.upvotes_count, 0)


class PublicationModelFieldsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création d'un profil
        cls.profile = baker.make(
            Profile,
            email="testadmin@example.com",
            slug=f"'testadmin@example.com'{uuid_generator()}",
            username="testadmin",
            profile_picture="picture.jpg",
        )
        cls.profile.set_password("testpasYEF93*&5sword")
        cls.profile.save()

        # Création d'une instance de Publication avec une histoire textuelle
        cls.text_publication = baker.make(
            Publication,
            title="Text Story",
            author_username=cls.profile.username,
            author_slug=cls.profile.slug,
            picture="picture.jpg",
            voice_story=None,
            text_story="This is a text story.",
            content_type=ContentTypes.text.value[0],
            # Fill in the rest of the fields as needed
        )

        # Création d'une instance de Publication avec une histoire vocale
        cls.voice_publication = baker.make(
            Publication,
            title="Voice Story",
            author_username=cls.profile.username,
            author_slug=cls.profile.slug,
            picture="picture.jpg",
            voice_story="voice.mp3",
            text_story=None,
            content_type=ContentTypes.voice.value[0],
            # Fill in the rest of the fields as needed
        )

    def test_text_publication(self):
        self.assertEqual(str(self.text_publication), "Text Story")
        self.assertEqual(
            self.text_publication.get_absolute_url(),
            reverse("users:account", args=[self.text_publication.author_slug]),
        )
        self.assertEqual(self.text_publication.content_type, ContentTypes.text.value[0])

    def test_voice_publication(self):
        self.assertEqual(str(self.voice_publication), "Voice Story")
        self.assertEqual(
            self.voice_publication.get_absolute_url(),
            reverse("users:account", args=[self.voice_publication.author_slug]),
        )
        self.assertEqual(
            self.voice_publication.content_type, ContentTypes.voice.value[0]
        )


class PublicationModelAllFieldsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Création d'un profil
        cls.profile = baker.make(
            Profile,
            email="testadmin@example.com",
            slug=f"'testadmin@example.com'{uuid_generator()}",
            username="testadmin",
            profile_picture="picture.jpg",
        )
        cls.profile.set_password("testpasYEF93*&5sword")
        cls.profile.save()

        # Création d'une instance de Publication avec tous les champs remplis
        cls.full_publication = baker.make(
            Publication,
            title="Full Story",
            author_username=cls.profile.username,
            author_slug=cls.profile.slug,
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
        )
        cls.full_publication.save()

    def test_full_publication(self):
        self.assertEqual(str(self.full_publication), "Full Story")
        self.assertEqual(
            self.full_publication.get_absolute_url(),
            reverse("users:account", args=[self.full_publication.author_slug]),
        )
        self.assertEqual(self.full_publication.content_type, ContentTypes.text.value[0])
        self.assertEqual(self.full_publication.season_of_stay, "Winter")
        self.assertEqual(self.full_publication.year_of_stay, 2000)
        self.assertEqual(self.full_publication.summary, "This is a summary.")
        self.assertEqual(self.full_publication.text_story, "This is a full story.")
        self.assertEqual(self.full_publication.upvotes_count, 0)
        self.assertIsNotNone(self.full_publication.created_at)
        self.assertIsNotNone(self.full_publication.updated_at)
        self.assertEqual(
            self.full_publication.created_at.date(),
            self.full_publication.updated_at.date(),
        )
