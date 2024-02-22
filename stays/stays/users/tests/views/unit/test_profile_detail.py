import pytest
from django.urls import reverse
from model_bakery import baker
from users.models import Profile
from django.contrib.messages import get_messages
from unittest.mock import patch
from icecream import ic
from django.test import override_settings
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from stays.utils.common_helpers import uuid_generator
User = get_user_model()


@override_settings(CSRF_COOKIE_SECURE=False, CSRF_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False)
@pytest.mark.django_db
class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)  # Disable CSRF checks
        
        self.user1 = baker.make(User, email='testeurdeouf@example.com')
        self.user1.set_password('testpassword')
        self.user1.username = 'testeurdeouf'
        self.user1.slug = f"testeurdeouf{uuid_generator()}"

        self.user1.save()
        self.user1_profile_url = reverse('users:profile', kwargs={'slug': self.user1.slug})

        self.user2 = baker.make(User, email='testeurpro@example.com')
        self.user2.set_password('test_pKassword82312!')
        self.user2.username = 'testeurpro'
        self.user2.slug = f"testeurpro{uuid_generator()}"
        self.user2.save()


    def test_with_unauthenticated_user(self):
        # Log in the user
        # self.client.login(email=self.user1.email, password='testpassword')
        ic(self.user1.slug)
        ic(self.user1_profile_url)
        ic(self.user2.slug)
        response = self.client.get(self.user1_profile_url, secure=False)
        ic(response)
        # Check the status code
        assert response.status_code == 200

        # # Check the template used
        # self.assertTemplateUsed(response, 'profile.html')

        # Check the context data
        context = response.context
        assert 'user' in context
        assert context['user'] == self.user1
        assert 'page_viewer_follows_profile' in context
        assert context['page_viewer_follows_profile'] is False
        assert 'viewer_follow_button' in context
        assert ">FOLLOW ME<" in context['viewer_follow_button']



    @patch('users.signals.update_user_status')
    def test_with_unauthenticated_user(self, mock_update_user_status):
        self.client.force_login(self.user2)
        ic(self.user2.slug)
        response = self.client.get(self.user1_profile_url, secure=False)
        ic(response)
        # Check the status code
        assert response.status_code == 200

        # Check the messages
        # messages = list(get_messages(response.wsgi_request))
        # assert len(messages) == 1
        # assert str(messages[0]) == 'Profile detail view accessed successfully.'

        # Check the signal was called
        # mock_signal.assert_called_once_with(sender=Profile, instance=profile)

        # Print the response content for debugging
        ic(response.content)