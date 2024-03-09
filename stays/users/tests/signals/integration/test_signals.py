from django.test import TestCase
from django.contrib.auth.hashers import make_password
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory

from unittest import mock


class TestUserLoginLogoutSignals(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password=make_password("password")
        )

    @mock.patch("users.signals.update_user_status")
    def test_user_logged_in_signal(self, mock_update_user_status):
        request = self.factory.get("/fake-path")
        user_logged_in.send(sender=self.__class__, user=self.user, request=request)
        mock_update_user_status.assert_called_once_with(self.user.email, True)

    @mock.patch("users.signals.update_user_status")
    def test_user_logged_out_signal(self, mock_update_user_status):
        request = self.factory.get("/fake-path")
        user_logged_out.send(sender=self.__class__, user=self.user, request=request)
        mock_update_user_status.assert_called_once_with(self.user.email, False)
