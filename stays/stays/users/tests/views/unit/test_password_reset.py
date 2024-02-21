import pytest
from django.test import override_settings
from django.test import TestCase, Client
from django.http import HttpResponseRedirect
from django.urls import reverse, resolve
from users.views import PasswordResetView
from users.forms import PasswordResetForm
from django.contrib.messages import get_messages
from model_bakery import baker
from django.conf import settings
from stays.utils.common_helpers import uuid_generator
from icecream import ic
from django.contrib.auth import get_user_model
User = get_user_model()


@override_settings(CSRF_COOKIE_SECURE=False, CSRF_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False)
@pytest.mark.django_db
class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = baker.make(User, email=settings.DEFAULT_EMAIL_DESTINATION)
        self.user.set_password('testpassword')
        self.user.username = 'testeurdeouf'
        # self.user.slug = f"testeurdeouf{uuid_generator()}"
        self.user.save()

    def test_view_class(self):
        response = self.client.get(reverse('users:password_reset'))
        assert response.status_code == 200

    def test_view_success_url_user_does_not_exist(self):
        form_data = {'email': 'test@example.com'}
        response = self.client.post(reverse('users:password_reset'), form_data)
        self.assertEqual(response.status_code, 200)
        # Get the messages from the response
        messages = list(get_messages(response.wsgi_request))

        # Check that there is exactly one message
        self.assertEqual(len(messages), 2)

        # Check that the message is an error
        self.assertEqual(messages[0].level_tag, 'error')
        expected_message = f"No user found with email {form_data['email']}"
        self.assertEqual(str(messages[0]), expected_message)

        self.assertEqual(messages[1].level_tag, 'error')
            

    def test_view_success_url_user_does_exist(self):
        form_data = {'email': settings.DEFAULT_EMAIL_DESTINATION}
        response = self.client.post(reverse('users:password_reset'), form_data)
        assert response.status_code == 302
        self.assertRedirects(response, reverse('users:password_reset_done'))