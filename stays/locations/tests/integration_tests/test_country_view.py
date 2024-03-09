import pytest
from asgiref.sync import sync_to_async
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.cache import cache
from django.test import AsyncClient, RequestFactory
from django.urls import reverse
from django.utils import timezone
from icecream import ic

from users.models import Profile


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


def add_session_to_request(request):
    """Annotate a request object with a session."""
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_country_good_code():
    # Set up the test client
    client = AsyncClient()

    # Create a user and authenticate the request
    create_user = sync_to_async(Profile.objects.create_user, thread_sensitive=True)
    user = await create_user(
        email="testuser@test.com", username="mike375P", password="12345"
    )
    # client.headers = {'Authorization': f'Bearer {user.auth_token}'}
    # Use sync_to_async to run force_login in a separate thread
    force_login = sync_to_async(client.force_login, thread_sensitive=True)
    await force_login(user)

    response = await client.get(reverse("locations:country", args=["FR"]))

    # Check that the response has a status code of 200
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.content.decode()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_country_good_code_context():
    # Create an instance of the request factory
    # Create an instance of the async client
    client = AsyncClient()
    factory = RequestFactory()

    # Create an instance of a GET request
    # request = factory.get('/country/FR')
    # Add session to the request
    add_session_to_request_async = sync_to_async(
        add_session_to_request, thread_sensitive=True
    )
    await add_session_to_request_async(factory.get("/country/FR"))

    # Create a user and add it to the request
    create_user = sync_to_async(Profile.objects.create_user, thread_sensitive=True)
    user = await create_user(
        email="testcontext@test.com", username="boBy96715", password="12345paw"
    )
    user.last_login = timezone.now()  # Set last_login to the current time

    # Save the user
    save_user = sync_to_async(user.save, thread_sensitive=True)
    await save_user()

    # Force login the user
    force_login = sync_to_async(client.force_login, thread_sensitive=True)
    await force_login(user)

    # Use the client to get a response from the view
    response = await client.get("/country/RO")
    ic(response)

    # Check that 'general_information' is in the response context
    assert "general_information" in response.context
    assert "air" in response.context
    assert "weather" in response.context
    assert "country_time" in response.context
