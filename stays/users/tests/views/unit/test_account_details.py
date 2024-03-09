import pytest
from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker
from unittest.mock import patch
from stays.utils.common_helpers import uuid_generator
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAccountDetailsView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF checks
        self.user = baker.make(User, email="testeurdeouf@example.com")
        self.user.username = "testeurdeouf"
        self.user.slug = f"testeurdeouf{uuid_generator()}"
        self.user.set_password("testpasswordP9671!")
        self.user.save()
        self.url = reverse("users:account", kwargs={"slug": self.user.slug})

    @patch("django.contrib.auth.mixins.LoginRequiredMixin", new_callable=lambda: object)
    @patch("users.signals.update_user_status")
    def test_account_details_with_authenticated_user(
        self, mock_update_user_status, mock_mixin
    ):
        # self.client.login(email=self.user.email, password='testpasswordP9671!')  # Log in the user
        self.client.force_login(self.user)

        response = self.client.get(self.url, secure=False)

        self.assertEqual(
            response.status_code, 200
        )  # Check that the user can access the page
        self.assertTemplateUsed(response, "account.html")  # Check the template

        self.assertIn("current_user", response.context)  # Check the context
        self.assertEqual(
            response.context["current_user"], self.user
        )  # Check the current user
        self.assertIsInstance(
            response.context["current_user"], User
        )  # Check the current user
        self.assertIn("number_of_publications", response.context)
        self.assertIsInstance(response.context["number_of_publications"], int)
        self.assertIn("number_of_followers", response.context)
        self.assertIsInstance(response.context["number_of_followers"], int)
        self.assertIn("number_of_following", response.context)
        self.assertIsInstance(response.context["number_of_following"], int)
        self.assertIn("profile_has_followers", response.context)
        self.assertIsInstance(response.context["profile_has_followers"], bool)
        self.assertIn("profile_follows_stayers", response.context)
        self.assertIsInstance(response.context["profile_follows_stayers"], bool)

    @patch("django.contrib.auth.mixins.LoginRequiredMixin", new_callable=lambda: object)
    @patch("users.signals.update_user_status")
    def test_account_details_authenticated_user_wrong_slug(
        self, mock_update_user_status, mock_mixin
    ):
        # self.client.login(email=self.user.email, password='testpasswordP9671!')  # Log in the user
        self.client.force_login(self.user)

        response = self.client.get(self.url[:-7], secure=False)
        self.assertNotIn("location", response)
        self.assertNotIn("Stays of", response.content.decode("utf-8"))
        self.assertTrue(
            "404-not-found.png" in response.content.decode()
            or "/* 1. BODY */" in response.content.decode()
        )

    def test_account_details_without_authenticated_user(self):
        response = self.client.get(self.url, secure=False)
        self.assertEqual(
            response.status_code, 302
        )  # Check that the user is redirected to the login page
