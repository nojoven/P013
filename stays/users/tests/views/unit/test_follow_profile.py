import pytest
from django.urls import reverse
from model_bakery import baker
from django.contrib.messages import get_messages
from unittest.mock import patch
from django.test import override_settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from stays.utils.common_helpers import uuid_generator
from friendship.models import Follow
import json

User = get_user_model()


@override_settings(CSRF_COOKIE_SECURE=False, CSRF_COOKIE_HTTPONLY=False, SESSION_COOKIE_SECURE=False)
@pytest.mark.django_db
class ProfileDetailViewTest(TestCase):
    def setUp(self):
        # Disable CSRF checks
        self.client = Client(enforce_csrf_checks=False)
        self.client2 = Client(enforce_csrf_checks=False)

        self.user1 = baker.make(User, email='testeurdeouf@example.com')
        self.user1.set_password('testpassword')
        self.user1.username = 'testeurdeouf'
        self.user1.slug = f"testeurdeouf{uuid_generator()}"
        self.user1.continent_of_birth = 'EU'

        self.user1.save()
        self.user1_profile_url = reverse('users:profile', kwargs={'slug': self.user1.slug})

        self.user2 = baker.make(User, email='testeurpro@example.com')
        self.user2.set_password('test_pKassword82312!')
        self.user2.username = 'testeurpro'
        self.user2.slug = f"testeurpro{uuid_generator()}"
        self.user2.continent_of_birth = 'EU'
        self.user2.save()


    @patch('users.signals.update_user_status')
    def test_follow_profile(self, mock_update_user_status):
        self.client.force_login(self.user2)

        follow_profile_url = reverse('users:follow_unfollow', kwargs={'slug': self.user1.slug})

        # Prepare the data to send in the request
        data = {
            'asking': self.user2.slug,
            'target': self.user1.slug,
            'relation': 'follow'
        }

        # Send a POST request to the follow_profile view
        response = self.client.post(follow_profile_url, json.dumps(data), content_type='application/json')

        # Check the status code
        assert response.status_code == 201

        # Check that self.user2 is now following self.user1
        assert Follow.objects.follows(self.user2, self.user1)

        # Check the success message
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == f"You are now following {self.user1.username}"


    @patch('users.signals.update_user_status')
    def test_unfollow_profile(self, mock_update_user_status):
        self.client.force_login(self.user2)

        # Make self.user2 follow self.user1
        Follow.objects.add_follower(self.user2, self.user1)

        follow_profile_url = reverse('users:follow_unfollow', kwargs={'slug': self.user1.slug})

        # Prepare the data to send in the request
        data = {
            'asking': self.user2.slug,
            'target': self.user1.slug,
            'relation': 'unfollow'
        }

        # Send a POST request to the follow_profile view
        response = self.client.post(follow_profile_url, json.dumps(data), content_type='application/json')

        # Check the status code
        assert response.status_code == 204

        # Check that self.user2 is not following self.user1
        assert not Follow.objects.follows(self.user2, self.user1)

        # Check the success message
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == f"You have unfollowed {self.user1.username}"


    @patch('users.signals.update_user_status')
    def test_follow_profile_invalid_relation(self, mock_update_user_status):
        self.client.force_login(self.user2)

        follow_profile_url = reverse('users:follow_unfollow', kwargs={'slug': self.user1.slug})

        # Prepare the data to send in the request
        data = {
            'asking': self.user2.slug,
            'target': self.user1.slug,
            'relation': 'invalid'
        }

        # Send a POST request to the follow_profile view
        response = self.client.post(follow_profile_url, json.dumps(data), content_type='application/json', follow=True)

        # Status 400 redirects successfully to error page with code 200 
        assert response.status_code == 200
