import pytest
from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker
from unittest.mock import patch
from stays.utils.common_helpers import uuid_generator
from django.contrib.auth import get_user_model
from icecream import ic

User = get_user_model()

@pytest.mark.django_db
class TestProfileStaysListView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF checks
        self.user = baker.make(User, email='testeurdeouf@example.com')
        self.user.set_password('testpassword')
        self.user.username = 'testeurdeouf'
        self.user.slug = f"testeurdeouf{uuid_generator()}"
        self.user.save()
        self.url = reverse('users:stays', kwargs={'slug': self.user.slug})

    @patch('users.signals.update_user_status')
    def test_stays_with_authenticated_user(self, mock_update_user_status):
        # Log in the user 
        # self.client.login(email=self.user.email, password='testpassword')
        self.client.force_login(self.user)
        response = self.client.get(self.url, secure=False)
        self.assertIsNotNone(response.context)
        self.assertEqual(response.status_code, 200)  # Check that the user can access the page
        self.assertTemplateUsed(response, 'stays.html')  # Check the template
        self.assertIn('publications', response.context)  # Check the context
        self.assertIn('page_obj', response.context)  # Check the context

    def test_stays_without_authenticated_user(self):
        response = self.client.get(self.url, secure=False)
        ic(response)
        ic(response.templates)
        ic(response.url)

        ic(response.content.decode('utf-8'))
        ic(response.status_code)
        self.assertEqual(response.status_code, 302)  # Check that the user is redirected to the login page
        self.assertIn('login', response.url)

    # @patch('users.signals.update_user_status')
    # def test_stays_with_non_existent_user(self, mock_update_user_status):
    #     self.client.login(email='testeurdeouf@example.com', password='testpassword')  # Log in the user
    #     url = reverse('users:stays', kwargs={'slug': 'nonexistent'})  # This user does not exist
    #     response = self.client.get(url, secure=False)
    #     ic(response.status_code)
    #     self.assertEqual(response.status_code, 404)  # Check that the server returns a 404 error

