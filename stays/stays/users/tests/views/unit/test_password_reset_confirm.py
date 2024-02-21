import pytest
from django.test import override_settings
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from model_bakery import baker
from django.contrib.auth import get_user_model

User = get_user_model()

class TestTokenGenerator(PasswordResetTokenGenerator):
    def check_token(self, user, token):
        # Ignore the token and always return True
        return True


@override_settings(CSRF_COOKIE_SECURE=False, CSRF_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False)
@pytest.mark.django_db
class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = baker.make(User, email=settings.DEFAULT_EMAIL_DESTINATION)
        self.user.set_password('testpassword')
        self.user.username = 'testeurpro'
        self.user.save()

        # Generate a reusable token
        self.token = TestTokenGenerator().make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.reset_page_url = reverse('users:password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})

        self.new_password_input_form_url = f"/password/reset/{self.uid}/set-password"

    def test_view_reachable(self):
        response = self.client.get(self.new_password_input_form_url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        form_data = {'new_password1': 'newpassword', 'new_password2': 'newpassword'}
        get_response = self.client.get(self.new_password_input_form_url)
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(self.reset_page_url, form_data)
        self.assertEqual(post_response.status_code, 302)

    def test_password_reset_passwords_mismatch(self):
        form_data = {'new_password1': 'newpas_sword', 'new_password2': 'n_ewpas_swor_d'}
        response = self.client.post(self.new_password_input_form_url, form_data)
        self.assertEqual(response.status_code, 200)
