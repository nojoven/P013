import pytest
from model_bakery import baker

from core.models import Publication
from users.models import Profile


@pytest.fixture
def mock_profile():
    return baker.make(Profile, _fill_optional=True)


@pytest.fixture
def mock_publication():
    return baker.make(Publication, _fill_optional=True)
