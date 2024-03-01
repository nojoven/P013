
import pytest
from icecream import ic
from django.urls import reverse
from model_bakery import baker
from users.models import Profile
from unittest import mock
from stays.utils.common_helpers import uuid_generator
from django_webtest import WebTest


class TestDeleteProfileView(WebTest):
    def setUp(self):
        self.user = baker.make('users.Profile', email='testuser@example.com', slug=f"testuser{uuid_generator()}")
        self.user.set_password('password')  # Définissez le mot de passe en clair
        self.user.save()

    @mock.patch('users.signals.update_user_status')
    @pytest.mark.django_db
    def test_delete_profile_view_with_owner(self, mock_update_user_status):
        self.client.force_login(self.user)
        ic(self.user.is_authenticated)
        response = self.client.get(reverse('users:delete_account', kwargs={'slug': self.user.slug}))
        assert response.status_code == 200
        assert response.context is not None
        assert "profile" in response.context
        assert response.context.get("profile") is not None
        assert isinstance(response.context.get("profile"), Profile)
        assert response.templates[0].name == 'delete_account.html'
        self.assertContains(response, '<button type="submit" class="btn btn-danger">Confirm</button>', html=True)

    @mock.patch('users.signals.update_user_status')
    @pytest.mark.django_db
    def test_delete_profile_view_post(self, mock_update_user_status):
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:delete_account', kwargs={'slug': self.user.slug}))
        

        # Check if the user is redirected to the success URL
        assert response.status_code == 302
        assert response.url == reverse('core:home')

        # Check if the user's profile has been deleted
        with pytest.raises(Profile.DoesNotExist):
            self.user.refresh_from_db()
