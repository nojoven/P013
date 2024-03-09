import pytest
from model_bakery import baker
from users.models import Profile
from core.models import Publication


@pytest.fixture
def mock_profile():
    return baker.make(Profile, _fill_optional=True)


@pytest.fixture
def mock_publication():
    return baker.make(Publication, _fill_optional=True)
