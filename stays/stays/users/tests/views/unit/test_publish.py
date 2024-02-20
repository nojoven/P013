import pytest
from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker
from unittest.mock import patch
from django.contrib.auth import get_user_model
from stays.utils.common_helpers import uuid_generator
from cleantext import clean
from icecream import ic

User = get_user_model()



@pytest.mark.django_db
class TestUpdateAccountView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF checks
        self.user = baker.make(User, email='testeurdeouf@example.com')
        self.user.set_password('testpassword')
        self.user.username = 'testeurdeouf'
        self.user.slug = f"testeurdeouf{uuid_generator()}"
        self.user.save()
        self.url = reverse('users:settings', kwargs={'slug': self.user.slug})

    @patch('users.signals.update_user_status')
    def test_reach_publish_page_with_authenticated_user(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        response = self.client.get(self.url)
        ic(response.status_code)
        self.assertEqual(response.status_code, 200)  # Check that the user can access the page
        self.assertTemplateUsed(response, 'settings.html')  # Check the template
        self.assertIsNotNone(response.context)  # Check the context
        self.assertIn('form', response.context)  # Check the context
        self.assertIn('current_user', response.context)  # Check the context
        self.assertIsInstance(response.context['current_user'], User)  # Check the current user

    def test_reach_publish_page_without_authenticated_user(self):
        response = self.client.get(self.url)
        ic(response.status_code)
        self.assertEqual(response.status_code, 302)  # Check that the user is redirected to the login page
