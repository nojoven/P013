from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from icecream import ic
from model_bakery import baker

from stays.utils.common_helpers import uuid_generator

User = get_user_model()


@pytest.mark.django_db
class TestAccountLoginView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.url = reverse("users:login")
        self.user = baker.make(User, email="testeurdeouf@example.com")
        self.user.set_password("testpasswordT9990!")
        self.user.username = "testeurdeouf"
        self.user.slug = f"testeurdeouf{uuid_generator()}"
        self.user.save()

    @patch("users.signals.update_user_status")
    def test_login_with_valid_form(self, mock_update_user_status):
        form_data = {
            "username": self.user.email,
            "password": "testpasswordT9990!",
        }
        assert User.objects.filter(email=self.user.email).exists()
        assert User.objects.filter(username=self.user.username).exists()
        response = self.client.post(self.url, form_data, secure=False)
        ic(response.status_code)
        self.assertEqual(response.status_code, 302)  # Check that the user is redirected
        mock_update_user_status.assert_called_once()  # Check that the signal was called

    def test_login_with_invalid_form(self):
        form_data = {
            "username": self.user.email,
            "password": "wrongpassword",  # Incorrect password
        }
        response = self.client.post(self.url, form_data, secure=False)
        ic(response.status_code)
        self.assertEqual(
            response.status_code, 200
        )  # Check that the user stays on the same page
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(
            str(messages[0]), "Something went wrong. Please check your input (  all  )."
        )  # Check the error message

    def test_login_with_non_existent_user(self):
        form_data = {
            "username": "nonexistent@example.com",  # This user does not exist
            "password": "testpassword",
        }
        response = self.client.post(self.url, form_data, secure=False)
        ic(response.status_code)
        self.assertEqual(
            response.status_code, 200
        )  # Check that the user stays on the same page
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(
            str(messages[0]), "Something went wrong. Please check your input (  all  )."
        )  # Check the error message


@pytest.mark.django_db
class TestAccountLoginViewFromFeed(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF checks
        self.url = reverse("users:login") + "?fromfeed=fromfeed"
        self.user = baker.make(User, email="test@example.com")
        self.user.set_password("testpassword")
        self.user.save()

    def test_login_with_invalid_form_fromfeed(self):
        form_data = {
            "username": "test@example.com",
            "password": "wrongpassword",  # Incorrect password
        }
        response = self.client.post(self.url, form_data, secure=False)
        ic(response.status_code)
        self.assertEqual(
            response.status_code, 200
        )  # Check that the user stays on the same page
        self.assertEqual(
            response.json(), {"error": "Invalid username or password"}
        )  # Check the error message
