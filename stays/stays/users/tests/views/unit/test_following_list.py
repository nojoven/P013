import pytest
from django.urls import reverse
from model_bakery import baker
from unittest.mock import patch
from django.test import override_settings
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from stays.utils.common_helpers import uuid_generator
from friendship.models import Follow
from django.db.models import Count

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
    def test_following_list_view(self, mock_update_user_status):
        self.client.force_login(self.user2)

        # Make self.user2 follow self.user1
        Follow.objects.add_follower(self.user2, self.user1)

        following_list_url = reverse('users:following', kwargs={'slug': self.user2.slug})

        response = self.client.get(following_list_url, secure=False)

        # Check the status code
        assert response.status_code == 200

        # Check the template used
        self.assertTemplateUsed(response, 'following.html')

        # Check the context data
        context = response.context
        assert 'stayers' in context
        assert context['stayers'].count() == 1
        assert context['stayers'].first().followee == self.user1
        assert 'follower_of_stayer' in context
        assert context['follower_of_stayer'] == self.user2.slug
        assert 'username_of_follower' in context
        assert context['username_of_follower'] == self.user2.username