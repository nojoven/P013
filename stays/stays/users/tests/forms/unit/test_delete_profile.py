import pytest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from test_plus.test import TestCase
from model_bakery import baker
from users.forms import DeleteProfileForm
from django.contrib.auth.hashers import make_password

class TestDeleteProfileForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = baker.make('users.Profile', email='user1@example.com', password=make_password('password'), username='user1Tester')
    @patch('users.forms.DeleteProfileForm.clean_username')
    def test_form_valid(self, mock_clean_username):
        mock_clean_username.return_value = 'user1@example.com'
        form = DeleteProfileForm({
            'email': 'user1@example.com',
        })
        assert form.is_valid()

    @patch('users.forms.DeleteProfileForm.clean_username')
    def test_form_invalid_username(self, mock_clean_username):
        mock_clean_username.return_value = 'wronguser@example.com'
        form = DeleteProfileForm({
            'email': 'wronguser@example.com',
        })
        assert not form.is_valid()
        assert 'email' in form.errors

    @patch('users.forms.DeleteProfileForm.clean_username')
    def test_form_username_empty(self, mock_clean_username):
        mock_clean_username.return_value = ''
        form = DeleteProfileForm({
            'email': '',
        })
        assert not form.is_valid()
        assert 'email' in form.errors