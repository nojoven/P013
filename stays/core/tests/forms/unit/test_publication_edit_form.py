import pytest
from django.urls import reverse
from django.test import TestCase
from django_webtest import WebTest
from model_bakery import baker
from stays.utils.common_helpers import uuid_generator
from datetime import datetime
from cities_light.models import Country
from core.forms import PublicationEditForm
from core.models import Publication
from users.models import Profile
from core.utils.models_helpers import ContentTypes
from uuid import uuid4
from unittest import mock
import io
from icecream import ic
from PIL import Image


class PublicationEditFormTest(WebTest, TestCase):
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

    def test_form_fields_required_for_voice_content_type(self):
        form = PublicationEditForm(instance=self.voice_publication)
        self.assertFalse(form.fields["text_story"].required)
        self.assertTrue(form.fields["voice_story"].required)
        self.assertFalse(form.fields["title"].required)
        self.assertFalse(form.fields["year_of_stay"].required)
        self.assertFalse(form.fields["season_of_stay"].required)
        self.assertFalse(form.fields["summary"].required)
        self.assertFalse(form.fields["country_code_of_stay"].required)
        self.assertFalse(form.fields["published_from_country_code"].required)
        self.assertFalse(form.fields["picture"].required)
        self.assertFalse(form.fields["upvotes_count"].required)
        self.assertFalse(form.fields["content_type"].required)

    def test_form_fields_required_for_text_content_type(self):
        form = PublicationEditForm(instance=self.text_publication)
        self.assertTrue(form.fields["text_story"].required)
        self.assertFalse(form.fields["voice_story"].required)

    @mock.patch("users.signals.update_user_status")
    @pytest.mark.django_db
    def test_form_with_valid_text_data(self, mock_update_user_status):
        response = self.app.get(
            reverse("core:edit_publication", args=[self.text_publication.uuid]),
            user=self.profile,
        )
        ic(response)
        ic(response.forms)
        form = response.forms[
            0
        ]  # replace 'form' with the actual form name if it's different
        ic(form.fields.keys())
        form["title"] = "Test Title"
        form["text_story"] = "Test Story"
        # form['picture'] = "new_pic.png"
        form["country_code_of_stay"] = "IT"
        form["year_of_stay"] = 1990
        form["season_of_stay"] = "Summer"
        form["summary"] = "A la piscine"

        # Create a new image of size 1x1
        image = Image.new("RGB", (1, 1))

        # Save the image to a BytesIO object
        file_like_object = io.BytesIO()
        image.save(file_like_object, format="PNG")
        # Get the bytes from the BytesIO object
        png_content = file_like_object.getvalue()
        # Now you can use `png_content` as a file content
        response = form.submit(
            upload_files=[("picture", "new_pic.png", png_content, "image/png")]
        )

        self.assertRedirects(
            response, reverse("core:publication", args=[self.text_publication.uuid])
        )

    @mock.patch("users.signals.update_user_status")
    @pytest.mark.django_db
    def test_form_with_valid_voice_data(self, mock_update_user_status):
        response = self.app.get(
            reverse("core:edit_publication", args=[self.text_publication.uuid]),
            user=self.profile,
        )
        ic(response)
        ic(response.forms)
        form = response.forms[
            0
        ]  # replace 'form' with the actual form name if it's different
        ic(form.fields.keys())
        form["title"] = "Test Title"
        form["text_story"] = "Test Story"
        # form['picture'] = "new_pic.png"
        form["country_code_of_stay"] = "IT"
        form["year_of_stay"] = 1990
        form["season_of_stay"] = "Summer"
        form["summary"] = "A la piscine"

        # Create a new BytesIO object
        file_like_object = io.BytesIO()

        # Write some bytes to it (for example, some random bytes)
        file_like_object.write(b"\x00\x01\x02\x03")

        # Get the bytes from the BytesIO object
        mp3_content = file_like_object.getvalue()

        # Now you can use `mp3_content` as a file content
        response = form.submit(
            upload_files=[("audio_file", "new_file.mp3", mp3_content, "audio/mpeg")]
        )

        self.assertRedirects(
            response, reverse("core:publication", args=[self.text_publication.uuid])
        )
