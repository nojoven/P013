import pytest
from django.test import RequestFactory
from users.models import Profile
from api import is_profile_online


# @pytest.mark.django_db
# def test_is_profile_online():
#     # Setup
#     factory = RequestFactory()
#     slug = 'test-slug'
#     Profile.objects.create(slug=slug, is_online=True)

#     request = factory.get(f"/isonline/{slug}/")

#     # Call the function
#     response = is_profile_online(request, slug)

#     # Check the response
#     assert response.status_code == 200
#     assert response.json() == {'is_online': True}