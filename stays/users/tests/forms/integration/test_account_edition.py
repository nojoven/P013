import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password
from faker import Faker
from cities_light.models import CONTINENT_CHOICES
from users.models import Profile
from users.forms import AccountEditionForm

fake = Faker()


@pytest.fixture
def profile():
    return Profile.objects.create_user(
        username="testuser",
        email="test@example.com",
        password=make_password("testpassword"),
    )


@pytest.fixture
def form_data(profile):
    return {
        "profile_picture": SimpleUploadedFile(
            "profile_pic.jpg", b"file_content", content_type="image/jpeg"
        ),
        "username": fake.user_name(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "season_of_birth": "Spring",
        "year_of_birth": fake.year(),
        "about_text": fake.text(),
        "motto": fake.sentence(),
        "signature": fake.sentence(),
        "continent_of_birth": CONTINENT_CHOICES[0][0],
        "email": "tester@users.net",
    }


@pytest.mark.django_db
def test_form_invalid_without_continent_of_birth(form_data):
    form = AccountEditionForm(data={})
    assert form.is_valid()


@pytest.mark.django_db
def test_form_valid(form_data):
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_username(form_data):
    form_data.pop("username")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_first_name(form_data):
    form_data.pop("first_name")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_last_name(form_data):
    form_data.pop("last_name")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_year_of_birth(form_data):
    form_data.pop("year_of_birth")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_about_text(form_data):
    form_data.pop("about_text")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_motto(form_data):
    form_data.pop("motto")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_signature(form_data):
    form_data.pop("signature")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_form_invalid_without_continent_of_birth(form_data):
    form_data.pop("continent_of_birth")
    form = AccountEditionForm(data=form_data)
    assert form.is_valid()
