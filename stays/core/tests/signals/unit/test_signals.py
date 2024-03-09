# Importations nécessaires pour les tests
from datetime import datetime
from model_bakery import baker
from stays.utils.common_helpers import uuid_generator
from django.test import TestCase
from locations.models import StayCountry
from cities_light.models import Country
from core.models import Publication, PublicationUpvote
from users.models import Profile, ProfileHasPublication
from core.utils.models_helpers import ContentTypes


class PublicationSignalTest(TestCase):
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
        self.country = Country.objects.create(name="Italy", code2="IT")

    def test_create_stay_country_on_publication_creation(self):
        # Création d'une instance de Publication
        publication = baker.make(
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
            country_code_of_stay=self.country.code2,
            published_from_country_code="FR",
            upvotes_count=0,
        )
        publication.save()

        # Vérification de la création d'une instance de StayCountry
        self.assertTrue(StayCountry.objects.filter(publication=publication).exists())


class PublicationUpvoteSignalTest(TestCase):
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
        self.country = Country.objects.create(name="Italy", code2="IT")

        # Création d'une instance de Publication
        self.publication = baker.make(
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
            country_code_of_stay=self.country.code2,
            published_from_country_code="FR",
            upvotes_count=0,
        )
        self.publication.save()

    def test_update_upvotes_count_on_publication_upvote_creation(self):
        self.assertEqual(self.publication.upvotes_count, 0)
        # Création d'une instance de PublicationUpvote
        publication_upvote = baker.make(
            PublicationUpvote,
            publication=self.publication,
            upvote_profile=self.profile.slug,
            upvote_value=1,
        )
        publication_upvote.save()

        # Rafraîchir l'instance de publication de la base de données
        self.publication.refresh_from_db()

        # Vérification de l'incrémentation de upvotes_count
        self.assertGreater(self.publication.upvotes_count, 0)


class ProfileHasPublicationSignalTest(TestCase):
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
        self.country = Country.objects.create(name="Italy", code2="IT")

    def test_create_profile_has_publication_on_publication_creation(self):
        # Création d'une instance de Publication
        publication = baker.make(
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
            country_code_of_stay=self.country.code2,
            published_from_country_code="FR",
            upvotes_count=0,
        )
        publication.save()

        # Vérification de la création d'une instance de ProfileHasPublication
        self.assertTrue(
            ProfileHasPublication.objects.filter(
                publication_of_user=publication
            ).exists()
        )
