from django.test import TestCase

from users.forms import RegistrationForm


class TestRegistrationForm(TestCase):
    def test_form_validity(self):
        # Testez la validité du formulaire avec des données correctes
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

        # Testez la validité du formulaire avec des données incorrectes
        data = {
            "username": "",
            "email": "testuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "",
            "password2": "testpassword123",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword123",
            "password2": "",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
