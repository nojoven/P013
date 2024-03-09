from django.test import TestCase
from django.contrib.auth import get_user_model
from users.forms import AccountLoginForm


class TestAccountLoginForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="password"
        )

    def test_form_valid(self):
        form = AccountLoginForm(
            data={"username": "testuser@example.com", "password": "password"}
        )
        self.assertTrue(form.is_valid())

    def test_form_no_email(self):
        form = AccountLoginForm(data={"password": "password"})
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_form_no_password(self):
        form = AccountLoginForm(data={"email": "testuser@example.com"})
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_form_invalid_email(self):
        form = AccountLoginForm(
            data={"email": "wronguser@example.com", "password": "password"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        error_message = form.errors["__all__"][0]  # Prenez le premier message d'erreur
        self.assertIn("email", error_message)

    def test_form_invalid_password(self):
        form = AccountLoginForm(
            data={"username": "testuser@example.com", "password": "wrongpassword"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        error_message = form.errors["__all__"][0]  # Prenez le premier message d'erreur
        self.assertIn("password", error_message)
