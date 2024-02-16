from django.test import TestCase
from django.contrib.auth import get_user_model
from users.forms import PasswordChangeFromConnectedProfile

class TestPasswordChangeFromConnectedProfile(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@test.com', password='old_password')

    def test_form_valid(self):
        form = PasswordChangeFromConnectedProfile(self.user, {
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_old_password(self):
        form = PasswordChangeFromConnectedProfile(self.user, {
            'old_password': 'wrong_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('old_password', form.errors)

    def test_form_passwords_do_not_match(self):
        form = PasswordChangeFromConnectedProfile(self.user, {
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'different_password',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors)

    def test_form_password_too_simple(self):
        form = PasswordChangeFromConnectedProfile(self.user, {
            'old_password': 'old_password',
            'new_password1': 'password',
            'new_password2': 'password',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors)