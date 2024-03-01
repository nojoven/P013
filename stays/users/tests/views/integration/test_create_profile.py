import pytest
from django.urls import reverse
from django.test import TestCase, Client
from model_bakery import baker
from django_webtest import WebTest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from unittest.mock import patch
from icecream import ic
from users.models import Profile
User = get_user_model()









@pytest.mark.django_db
class TestCreateProfileView(WebTest):
    csrf_checks = False
    def setUp(self):
        self.url = reverse('users:signup')

    @patch('users.signals.update_user_status')
    def test_create_profile_with_valid_form(self, mock_update_user_status):
        form_data = {
            'email': 'testerandadmin@examples.com',
            'username': 'testuserDuTest96',
            'password1': 'testPpassword985275Zf!',
            'password2': 'testPpassword985275Zf!',
        }
        response = self.app.post(self.url, form_data)
        ic(Profile.objects.all())
        # ic(list(get_messages(response.context['request'])))
        self.assertEqual(response.status_code, 302)  # Check that the user is redirected
        assert Profile.objects.get(email=form_data['email']) is not None  # Check that the user was created
        self.assertIn(response.location, "/login")
        # messages = list(get_messages(self.app.session))
        # self.assertEqual(len(messages), 1)
        # self.assertEqual(str(messages[0]), f"Welcome ! Your account is being created with your email address {form_data['email']} !")

    def test_create_profile_with_non_matching_passwords(self):
        form_data = {
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'differentpassword',  # Passwords don't match
            'username': 'testuserDuTest'
        }
        response = self.app.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)  # Check that the user stays on the same page
        self.assertFalse(User.objects.filter(email='test@example.com').exists())  # Check that the user was not created

    # def test_create_profile_with_existing_email(self):
    #     existing_user = baker.make(User, email='test@example.com')
    #     form_data = {
    #         'email': 'test@example.com',
    #         'password1': 'testpassword',
    #         'password2': 'testpassword',
    #     }
    #     response = self.app.post(self.url, form_data)
    #     self.assertEqual(response.status_code, 200)  # Check that the user stays on the same page
    #     messages = list(get_messages(response.context['request']))
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'Something went wrong. Please check your input (Email).')  # Check the error message




class TestCreateProfileViewMessages(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('users:signup')

    @patch('users.signals.update_user_status')
    def test_create_profile_with_success(self, mock_update_user_status):
        form_data = {
            'email': 'testerandadmin@examples.com',
            'username': 'testuserDuTest96',
            'password1': 'testPpassword985275Zf!',
            'password2': 'testPpassword985275Zf!',
        }
        response = self.client.post(self.url, form_data, follow=True)
        # self.assertEqual(response.status_code, 200)  # Check that the user is redirected
        # assert Profile.objects.get(email=form_data['email']) is not None  # Check that the user was created
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Welcome ! Your account is being created with your email address {form_data['email']} !")

        def test_create_profile_invalid_email_failure(self, mock_update_user_status):
            form_data = {
                'email': 'testerandadminexamplescom',
                'username': 'testuserDuTest96',
                'password1': 'testPpassword985275Zf!',
                'password2': 'testPpassword985275Zf!',
            }
            response = self.client.post(self.url, form_data, follow=True)
            # self.assertEqual(response.status_code, 200)  # Check that the user is redirected
            # assert Profile.objects.get(email=form_data['email']) is not None  # Check that the user was created
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(
                str(messages[0]),
                "Something went wrong. Please check your input (Email)."
            )

