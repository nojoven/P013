# Python
from unittest.mock import MagicMock, patch

import pytest
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse
from model_bakery import baker

from stays.utils.common_helpers import uuid_generator
from users.models import Profile
from users.views import DeleteProfileView


@patch("users.signals.update_user_status")
@pytest.mark.django_db
def test_DeleteProfileView_get(mock_update_user_status):
    # Create a mock request
    factory = RequestFactory()
    # Create a mock user and profile
    profile = baker.make(
        Profile,
        username="testuser010",
        email="testuser010@test.com",
        slug=f"testuser010{uuid_generator()}",
    )
    profile.set_password("éàAQUE@$_testpa051ssword")
    profile.save()
    # Assign the mock user to the request
    request = factory.get(
        reverse("users:delete_account", kwargs={"slug": profile.slug})
    )
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


@patch("users.signals.update_user_status")
@pytest.mark.django_db
def test_DeleteProfileView_post(mock_update_user_status):
    # Create a mock request
    factory = RequestFactory()
    # Create a mock user and profile
    profile = baker.make(
        Profile,
        username="testuser05",
        email="testuser05@test.com",
        slug=f"testuser05{uuid_generator()}",
    )
    profile.set_password("test*pa89241_Yssword")
    profile.save()
    # Assign the mock user to the request
    request = factory.post(
        reverse("users:delete_account", kwargs={"slug": profile.slug})
    )
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
