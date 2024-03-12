import pytest
import re
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from icecream import ic
from model_bakery import baker
from neattext.functions import clean_text
from stays.utils.common_helpers import uuid_generator

User = get_user_model()


@pytest.mark.django_db
class TestUpdateAccountView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF checks
        self.user = baker.make(User, email="testeurdeouf@example.com")
        self.user.set_password("testpassword")
        self.user.username = "testeurdeouf"
        self.user.slug = f"testeurdeouf{uuid_generator()}"
        self.user.save()
        self.url = reverse("users:settings", kwargs={"slug": self.user.slug})

    @patch("users.signals.update_user_status")
    def test_update_account_with_authenticated_user(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        response = self.client.get(self.url)
        ic(response.status_code)
        self.assertEqual(
            response.status_code, 200
        )  # Check that the user can access the page
        self.assertTemplateUsed(response, "settings.html")  # Check the template
        self.assertIsNotNone(response.context)  # Check the context
        self.assertIn("form", response.context)  # Check the context
        self.assertIn("current_user", response.context)  # Check the context
        self.assertIsInstance(
            response.context["current_user"], User
        )  # Check the current user

    def test_update_account_without_authenticated_user(self):
        response = self.client.get(self.url)
        ic(response.status_code)
        self.assertEqual(
            response.status_code, 302
        )  # Check that the user is redirected to the login page

    @patch("users.signals.update_user_status")
    def test_update_account_form_submission(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        dirty_about_text = "Some dirty about text with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, and stopwords like 'the', 'is', 'in'."
        dirty_signature = "Some dirty signature with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, and stopwords like 'the', 'is', 'in'."
        form_data = {"about_text": dirty_about_text, "signature": dirty_signature}
        response = self.client.post(self.url, data=form_data, secure=False)
        ic(response.status_code)
        self.assertEqual(
            response.status_code, 302
        )  # Check that the form submission is successful
        self.user.refresh_from_db()
        ic(len(dirty_about_text))
        cleaned_about_text = clean_text(
            dirty_about_text,
            urls=True,
            emails=True,
            phone_num=True,
            stopwords=False,
            
        )
        # Split the original and cleaned text into words
        words_input = re.findall(r'\b[\w\'-]+\b', dirty_about_text)  # Use dirty_about_text here
        words = re.findall(r'\b[\w\'-]+\b', cleaned_about_text)

        # For each word in the cleaned text, check if an uppercase version of the word exists in the original text
        for i, word in enumerate(words):
            for word_input in words_input:
                if word.lower() == word_input.lower() and word_input[0].isupper():
                    # If an uppercase version of the word exists, replace the word with the uppercase version
                    words[i] = word_input
                    break

        # Join the words back into a string
        cleaned_about_text = ' '.join(words)
        ic(dirty_about_text)
        ic("becomes")
        ic(cleaned_about_text)
        ic("changes:")
        ic(
            set(dirty_about_text.split()).symmetric_difference(
                set(cleaned_about_text.split())
            )
        )
        ic(f"Something changed : {dirty_about_text != cleaned_about_text}")
        self.assertEqual(
            self.user.about_text, cleaned_about_text
        )  # Check that the profile was updated with cleaned text
        cleaned_signature = clean_text(
            dirty_signature,
            urls=True,
            emails=True,
            phone_num=True,
            stopwords=False,
            
        )
        # Split the original and cleaned text into words
        words_input = re.findall(r'\b[\w\'-]+\b', dirty_signature)
        words = re.findall(r'\b[\w\'-]+\b', cleaned_signature)

        # For each word in the cleaned text, check if an uppercase version of the word exists in the original text
        for i, word in enumerate(words):
            for word_input in words_input:
                if word.lower() == word_input.lower() and word_input[0].isupper():
                    # If an uppercase version of the word exists, replace the word with the uppercase version
                    words[i] = word_input
                    break

        # Join the words back into a string
        cleaned_signature = ' '.join(words)
        self.assertEqual(self.user.signature, cleaned_signature)
        # Get the messages from the response
        messages = list(get_messages(response.wsgi_request))

        # Check that there is exactly one message
        self.assertEqual(len(messages), 1)

        # Check that the message is what you expect
        self.assertEqual(str(messages[0]), "Profile updated successfully!")

        # Check the message's extra tags
        self.assertEqual(messages[0].extra_tags, "base_success")

    @patch("users.signals.update_user_status")
    def test_update_account_form_submission_empty_signature(
        self, mock_update_user_status
    ):
        self.client.force_login(self.user)  # Log in the user
        dirty_about_text = "Some NEW dirty about text with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, and stopwords like 'the', 'is', 'in'."
        form_data = {"about_text": dirty_about_text}
        response = self.client.post(self.url, data=form_data, secure=False)
        self.assertEqual(
            response.status_code, 302
        )  # Check that the form submission is successful
        self.user.refresh_from_db()
        cleaned_about_text = clean_text(
            dirty_about_text,
            urls=True,
            emails=True,
            phone_num=True,
            stopwords=False,
            
        )
        # Split the original and cleaned text into words
        words_input = re.findall(r'\b[\w\'-]+\b', dirty_about_text)
        words = re.findall(r'\b[\w\'-]+\b', cleaned_about_text)

        # For each word in the cleaned text, check if an uppercase version of the word exists in the original text
        for i, word in enumerate(words):
            for word_input in words_input:
                if word.lower() == word_input.lower() and word_input[0].isupper():
                    # If an uppercase version of the word exists, replace the word with the uppercase version
                    words[i] = word_input
                    break

        # Join the words back into a string
        cleaned_about_text = ' '.join(words)
        ic(dirty_about_text)
        ic("becomes")
        ic(cleaned_about_text)
        ic("changes:")
        ic(
            set(dirty_about_text.split()).symmetric_difference(
                set(cleaned_about_text.split())
            )
        )
        ic(f"Something changed : {dirty_about_text != cleaned_about_text}")
        self.assertEqual(
            self.user.about_text, cleaned_about_text
        )  # Check that the profile was updated with cleaned text

    @patch("users.signals.update_user_status")
    def test_update_account_form_submission_empty_about_text(
        self, mock_update_user_status
    ):
        self.client.force_login(self.user)  # Log in the user
        dirty_signature = "Some dirty signature with URLs like https://example.com, emails like test@example.com, phone numbers like +1-555-555-5555, numbers like 12345, currency symbols like $, multiple whitespaces, and stopwords like 'the', 'is', 'in'."
        form_data = {"signature": dirty_signature}
        response = self.client.post(self.url, data=form_data, secure=False)
        self.assertEqual(
            response.status_code, 302
        )  # Check that the form submission is successful
        self.user.refresh_from_db()
        cleaned_signature = clean_text(
            dirty_signature,
            urls=True,
            emails=True,
            phone_num=True,
            stopwords=False,
            
        )
        # Split the original and cleaned text into words
        words_input = re.findall(r'\b[\w\'-]+\b', dirty_signature)
        words = re.findall(r'\b[\w\'-]+\b', cleaned_signature)

        # For each word in the cleaned text, check if an uppercase version of the word exists in the original text
        for i, word in enumerate(words):
            for word_input in words_input:
                if word.lower() == word_input.lower() and word_input[0].isupper():
                    # If an uppercase version of the word exists, replace the word with the uppercase version
                    words[i] = word_input
                    break

        # Join the words back into a string
        cleaned_signature = ' '.join(words)
        self.assertEqual(self.user.signature, cleaned_signature)

    @patch("users.signals.update_user_status")
    def test_update_account_form_submission_empty_data(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        form_data = {}
        response = self.client.post(self.url, data=form_data, secure=False)
        self.assertEqual(
            response.status_code, 302
        )  # Check that the form submission is successful

    @patch("users.signals.update_user_status")
    def test_update_account_invalid_form(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        continent_of_birth = "UU"
        form_data = {"continent_of_birth": continent_of_birth}
        response = self.client.post(self.url, data=form_data, secure=False)
        ic(response.status_code)
        # Get the messages from the response
        messages = list(get_messages(response.wsgi_request))

        # Check that there is exactly one message
        self.assertEqual(len(messages), 1)

        # Check that the message is an error
        self.assertEqual(messages[0].level_tag, "error")

        # Check that the message text is what you expect
        expected_message = (
            "Something went wrong. Please check your input (Continent of birth)."
        )
        self.assertEqual(str(messages[0]), expected_message)
