import pytest
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from model_bakery import baker
from unittest.mock import patch
from django.contrib.auth import get_user_model
from stays.utils.common_helpers import uuid_generator
from cleantext import clean
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from icecream import ic
from core.models import Publication

User = get_user_model()


@override_settings(CSRF_COOKIE_SECURE=False, CSRF_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False)
@pytest.mark.django_db
class TestPublishView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF checks
        self.user = baker.make(User, email='testeurdeouf@example.com')
        self.user.set_password('testpassword')
        self.user.username = 'testeurdeouf'
        self.user.slug = f"testeurdeouf{uuid_generator()}"
        self.user.save()
        self.url = reverse('users:publish', kwargs={'slug': self.user.slug})
        ic(self.url)



    @patch('users.signals.update_user_status')
    def test_reach_publish_page_with_authenticated_user(self, mock_update_user_status):
        self.client.force_login(self.user)  # Log in the user
        response = self.client.get(self.url, secure=False)
        # ic(response)
        # ic(response.status_code)
        # ic(response.content)
        # ic(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)  # Check that the user can access the page
        self.assertTrue(response.templates[0].name == 'publish.html')  # Check the template
        self.assertIsNotNone(response.context)  # Check the context
        self.assertIn('form', response.context)  # Check the context
        self.assertIn('active_from_contry_code', response.context)  # Check the context
        self.assertIn('active_from_contry_name', response.context)  # Check the context
        self.assertIsInstance(response.context['current_user'], User)  # Check the current user

    def test_reach_publish_page_without_authenticated_user(self):
        response = self.client.get(self.url)
        ic(response.status_code)
        self.assertEqual(response.status_code, 302)  # Check that the user is redirected to the login page
        self.assertIn('login', response.url)



    @patch('users.signals.update_user_status')
    def test_publish_view_text_story(self, mock_update_user_status):
        # Préparation des données du formulaire
        dirty_text_story = "Test MÃ©xico Story with a URL http://example.com, an email address test@example.com, and a phone number 123-456-7890."
        cleaned_text_story = clean(
            dirty_text_story,
            fix_unicode=True,               # fix various unicode errors
            to_ascii=False,                  # transliterate to closest ASCII representation
            lower=False,                     # lowercase text
            no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
            no_urls=True,                  # replace all URLs with a special token
            no_emails=True,                # replace all email addresses with a special token
            no_phone_numbers=True,         # replace all phone numbers with a special token
            no_numbers=False,               # replace all numbers with a special token
            no_digits=False,                # replace all digits with a special token
            no_currency_symbols=False,      # replace all currency symbols with a special token
            no_punct=False,                 # remove punctuations
            replace_with_punct="",          # instead of removing punctuations you may replace them
            replace_with_url="<URL>",
            replace_with_email="<EMAIL>",
            replace_with_phone_number="<PHONE>",
            replace_with_currency_symbol="<$£>",
            lang="en"                       # set to 'de' for German special handling
        )

        form_data = {
            'content_type': 'text',
            'title': 'México',
            'author_slug': self.user.slug,
            'author_username': self.user.username,
            'country_code_of_stay': 'FR',
            'published_from_country_code': 'FR',
            'summary': 'Test Summary',
            'picture': SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),
            'year_of_stay': 2022,
            'season_of_stay': 'Spring',
            'text_story': dirty_text_story
        }

        self.client.force_login(self.user)  # Log in the user
        # Soumission du formulaire
        response = self.client.post(self.url, form_data)

        # Vérification que la réponse est correcte
        self.assertEqual(response.status_code, 302)  # Redirection après la soumission du formulaire
        # Get the messages from the response
        messages = list(get_messages(response.wsgi_request))

        # Check that there is exactly one message
        self.assertEqual(len(messages), 1)

        # Check that the message is what you expect
        self.assertEqual(str(messages[0]), 'Publication created successfully!')

        # Check the message's extra tags
        self.assertEqual(messages[0].extra_tags, 'base_success')

        # Vérification que la publication a été enregistrée correctement
        publication = Publication.objects.get(content_type='text')
        publication.refresh_from_db()
        self.assertEqual(publication.title, form_data['title'])
        self.assertEqual(publication.author_username, self.user.username)
        self.assertEqual(publication.author_slug, self.user.slug)
        self.assertEqual(publication.country_code_of_stay, form_data['country_code_of_stay'])
        self.assertEqual(publication.published_from_country_code.code, form_data['published_from_country_code'])
        self.assertEqual(publication.summary, form_data['summary'])
        self.assertEqual(publication.picture.name.split("/")[-1], "file.jpg")
        self.assertEqual(publication.year_of_stay, form_data['year_of_stay'])
        self.assertEqual(publication.season_of_stay, form_data['season_of_stay'])
        self.assertEqual(publication.content_type, form_data['content_type'])
        self.assertEqual(publication.text_story, cleaned_text_story)
        self.assertTrue(self.client.session['force_renew_session'])

    @patch('users.signals.update_user_status')
    def test_publish_view_voice_story(self, mock_signal):
        # Préparation des données du formulaire
        form_data = {
            'content_type': 'voice',
            'title': 'Test Title',
            'author_slug': self.user.slug,
            'author_username': self.user.username,
            'country_code_of_stay': 'FR',
            'published_from_country_code': 'FR',
            'summary': 'Test Summary',
            'picture': SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),
            'year_of_stay': 2022,
            'season_of_stay': 'Spring',
            'voice_story': SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        }

        self.client.force_login(self.user)  # Log in the user
        # Soumission du formulaire
        response = self.client.post(self.url, form_data)

        # Vérification que la réponse est correcte
        self.assertEqual(response.status_code, 302)  # Redirection après la soumission du formulaire

        # Vérification que la publication a été enregistrée correctement
        publication = Publication.objects.get(content_type="voice")
        self.assertEqual(publication.title, 'Test Title')
        self.assertEqual(publication.author_username, self.user.username)
        self.assertIsNotNone(publication.voice_story)
        self.assertTrue(publication.text_story == '')
        self.assertEqual(publication.published_from_country_code.code, form_data['published_from_country_code'])
        self.assertTrue(self.client.session['force_renew_session'])

    @patch('users.signals.update_user_status')
    def test_publish_view_no_story(self, mock_update_user_status):
        # Préparation des données du formulaire

        form_data = {
            'content_type': 'text',
            'title': 'México',
            'author_slug': self.user.slug,
            'author_username': self.user.username,
            'country_code_of_stay': 'FR',
            'published_from_country_code': 'IT',
            'summary': 'Test Summary',
            'picture': SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg"),
            'year_of_stay': 2022,
            'season_of_stay': 'Spring'
        }

        self.client.force_login(self.user)  # Log in the user
        # Soumission du formulaire
        response = self.client.post(self.url, form_data)
        # Get the messages from the response
        messages = list(get_messages(response.wsgi_request))

        # Check that there is exactly one message
        self.assertEqual(len(messages), 2)

        # Check that the message is an error
        self.assertEqual(messages[0].level_tag, 'error')

        # Check that the message text is what you expect
        expected_message = 'Please provide either a text story OR a voice recording.'
        self.assertEqual(str(messages[0]), expected_message)
        default_message = 'Something went wrong. Please check your input'
        self.assertTrue(default_message in str(messages[1]))