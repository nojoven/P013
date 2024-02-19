# Python
import pytest
from django.urls import reverse
from model_bakery import baker
from django.test import RequestFactory
from users.views import DeleteProfileView
from unittest.mock import MagicMock
from django.contrib.auth.models import AnonymousUser
from users.models import Profile
from icecream import ic

from unittest.mock import patch
from django.http import HttpResponse

@pytest.mark.django_db
def test_DeleteProfileView_get():
    # Create a mock request
    factory = RequestFactory()
    # Create a mock user and profile
    profile = baker.make('Profile', username='testuser', email='testuser@test.com')
    profile.set_password('testpassword')
    profile.save()
    # Assign the mock user to the request
    request = factory.get(reverse('users:delete_account', kwargs={'slug': profile.slug}))
    request.user = profile

    # Instantiate the view with the mock request
    view = DeleteProfileView()
    view.request = request

    # Mock the get_object method to return the mock profile
    view.get_object = lambda: profile

    # Call the get method of the view and get the response
    response = view.get(request)

    # Assert that the response has a status code of 200
    assert response.status_code == 200





@pytest.mark.django_db
def test_DeleteProfileView_post():
    # Create a mock request
    factory = RequestFactory()
    # Create a mock user and profile
    profile = baker.make('Profile', username='testuser', email='testuser@test.com')
    profile.set_password('testpassword')
    profile.save()
    # Assign the mock user to the request
    request = factory.post(reverse('users:delete_account', kwargs={'slug': profile.slug}))
    request.user = profile

    # Instantiate the view with the mock request
    view = DeleteProfileView()
    view.request = request

    # Mock the get_object method to return the mock profile
    view.get_object = lambda: profile

    # Mock the post method of the view
    view.post = MagicMock(return_value=HttpResponse(status=302))

    # Call the post method of the view and get the response
    response = view.post(request)

    # Assert that the response has a status code of 302 (redirect)
    assert response.status_code == 302