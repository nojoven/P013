from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from friendship.models import Follow
from model_bakery import baker

from stays.utils.common_helpers import uuid_generator

User = get_user_model()


@override_settings(
    CSRF_COOKIE_SECURE=False, CSRF_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False
)
@pytest.mark.django_db
class ProfileDetailViewTest(TestCase):
    def setUp(self):
        # Disable CSRF checks
        self.client = Client(enforce_csrf_checks=False)
        self.client2 = Client(enforce_csrf_checks=False)

        self.user1 = baker.make(User, email="testeurdeouf@example.com")
        self.user1.set_password("testpassword")
        self.user1.username = "testeurdeouf"
        self.user1.slug = f"testeurdeouf{uuid_generator()}"
        self.user1.continent_of_birth = "EU"

        self.user1.save()
        self.user1_profile_url = reverse(
            "users:profile", kwargs={"slug": self.user1.slug}
        )

        self.user2 = baker.make(User, email="testeurpro@example.com")
        self.user2.set_password("test_pKassword82312!")
        self.user2.username = "testeurpro"
        self.user2.slug = f"testeurpro{uuid_generator()}"
        self.user2.continent_of_birth = "EU"
        self.user2.save()

    @patch("users.signals.update_user_status")
    def test_with_registered_viewer(self, mock_update_user_status):
        self.client.force_login(self.user2)

        assert User.objects.get(slug=self.user1.slug) is not None
        assert User.objects.get(slug=self.user2.slug) is not None

        response = self.client.get(self.user1_profile_url, secure=False)
        # Check the status code
        assert response.status_code == 200

        # # Check the template used
        self.assertTemplateUsed(response, "profile.html")

        # Check the context data
        context = response.context
        assert "user" in context
        assert context["user"].slug != self.user1.slug
        assert context["user"].slug == self.user2.slug
        assert ">FOLLOW ME<" in context["viewer_follow_button"]
        assert context["page_viewer_follows_profile"] is False

    def test_with_unregistered_user(self):
        response2 = self.client2.get(
            self.user1_profile_url,
            secure=False,
        )
        # Check the status code
        assert response2.status_code == 200
        assert "viewer_follow_button" not in response2.context

    @patch("users.signals.update_user_status")
    def test_with_registered_viewer_following(self, mock_update_user_status):
        self.client.force_login(self.user2)

        # Make self.user2 follow self.user1
        Follow.objects.add_follower(self.user2, self.user1)

        assert User.objects.get(slug=self.user1.slug) is not None
        assert User.objects.get(slug=self.user2.slug) is not None

        response = self.client.get(self.user1_profile_url, secure=False)

        # Check the status code
        assert response.status_code == 200

        # Check the context data
        context = response.context
        assert "user" in context
        assert context["user"].slug != self.user1.slug
        assert context["user"].slug == self.user2.slug
        assert ">FOLLOWING<" in context["viewer_follow_button"]
        assert context["page_viewer_follows_profile"] is True
