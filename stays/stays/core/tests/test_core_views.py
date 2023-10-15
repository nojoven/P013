import pytest
import logging
from django.test import TestCase
from core import views as core_views

LOGGER = logging.getLogger(__name__)




pytestmark = pytest.mark.django_db

# Create your tests here.
@pytest.mark.django_db(databases=['test'])
class TestCoreViews(TestCase):

    HOME_URI = "http://localhost:5000/"
    LOGOUT_URI = f"{HOME_URI}logout"

    def test_get_home(self):
        TestCase.databases = '__all__'
        response = self.client.get(self.HOME_URI)
        assert response.status_code == 200


    def test_logout(self):
        TestCase.databases = '__all__'
        response = self.client.get(self.LOGOUT_URI)

        assert response.status_code == 302


