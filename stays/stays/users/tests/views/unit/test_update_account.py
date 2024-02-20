import pytest
from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker
from unittest.mock import patch
from django.contrib.auth import get_user_model
from stays.utils.common_helpers import uuid_generator
from neattext.functions import clean_text
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
    def test_update_account_with_authenticated_user(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        response = self.client.get(self.url)
        ic(response.status_code)
        self.assertEqual(response.status_code, 200)  # Check that the user can access the page
        self.assertTemplateUsed(response, 'settings.html')  # Check the template
        self.assertIsNotNone(response.context)  # Check the context
        self.assertIn('form', response.context)  # Check the context
        self.assertIn('current_user', response.context)  # Check the context
        self.assertIsInstance(response.context['current_user'], User)  # Check the current user

    def test_update_account_without_authenticated_user(self):
        response = self.client.get(self.url)
        ic(response.status_code)
        self.assertEqual(response.status_code, 302)  # Check that the user is redirected to the login page



    @patch('users.signals.update_user_status')
    def test_update_account_form_submission(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        dirty_about_text = "Some dirty about text with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, special characters like @#%^&*, emojis like 😃, and stopwords like 'the', 'is', 'in'."
        dirty_signature = "Some dirty signature with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, special characters like @#%^&*, emojis like 😃, and stopwords like 'the', 'is', 'in'."
        form_data = {'about_text': dirty_about_text, 'signature': dirty_signature}
        response = self.client.post(self.url, data=form_data, secure=False)
        ic(response.status_code)
        self.assertEqual(response.status_code, 302)  # Check that the form submission is successful
        self.user.refresh_from_db()
        ic(len(dirty_about_text))
        cleaned_about_text = clean_text(dirty_about_text, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=False, multiple_whitespaces=True, special_char=False, emojis=False, stopwords=True)
        ic(dirty_about_text)
        ic("becomes")
        ic(cleaned_about_text)
        ic("changes:")
        ic(set(dirty_about_text.split()).symmetric_difference(set(cleaned_about_text.split())))
        ic(f"Something changed : {dirty_about_text != cleaned_about_text}")
        self.assertEqual(self.user.about_text, cleaned_about_text)  # Check that the profile was updated with cleaned text
        cleaned_signature = clean_text(dirty_signature, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=False, multiple_whitespaces=True, special_char=False, emojis=False, stopwords=True)
        self.assertEqual(self.user.signature, cleaned_signature)


    @patch('users.signals.update_user_status')
    def test_update_account_form_submission_empty_signature(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        dirty_about_text = "Some NEW dirty about text with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, special characters like @#%^&*, emojis like 😃, and stopwords like 'the', 'is', 'in'."
        form_data = {'about_text': dirty_about_text}
        response = self.client.post(self.url, data=form_data, secure=False)
        self.assertEqual(response.status_code, 302)  # Check that the form submission is successful
        self.user.refresh_from_db()
        cleaned_about_text = clean_text(dirty_about_text, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=False, multiple_whitespaces=True, special_char=False, emojis=False, stopwords=True)
        ic(dirty_about_text)
        ic("becomes")
        ic(cleaned_about_text)
        ic("changes:")
        ic(set(dirty_about_text.split()).symmetric_difference(set(cleaned_about_text.split())))
        ic(f"Something changed : {dirty_about_text != cleaned_about_text}")
        self.assertEqual(self.user.about_text, cleaned_about_text)  # Check that the profile was updated with cleaned text


    @patch('users.signals.update_user_status')
    def test_update_account_form_submission_empty_about_text(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        dirty_signature = "Some dirty signature with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, special characters like @#%^&*, emojis like 😃, and stopwords like 'the', 'is', 'in'."
        form_data = {'signature': dirty_signature}
        response = self.client.post(self.url, data=form_data, secure=False)
        self.assertEqual(response.status_code, 302)  # Check that the form submission is successful
        self.user.refresh_from_db()
        cleaned_signature = clean_text(dirty_signature, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=False, multiple_whitespaces=True, special_char=False, emojis=False, stopwords=True)
        self.assertEqual(self.user.signature, cleaned_signature)

    @patch('users.signals.update_user_status')
    def test_update_account_form_submission_empty_data(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        form_data = {}
        response = self.client.post(self.url, data=form_data, secure=False)
        self.assertEqual(response.status_code, 302)  # Check that the form submission is successful

