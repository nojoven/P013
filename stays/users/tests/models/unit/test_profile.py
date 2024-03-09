import pytest
from django.urls import reverse
from django.utils.text import slugify
from model_bakery import baker

from users.models import Profile


@pytest.mark.django_db
class TestUserManager:
    def setup_method(self):
        self.manager = Profile.objects

    def test_create_user(self):
        user = self.manager.create_user("user2@example.com", "password")
        assert user.email == "user2@example.com"
        assert user.check_password("password")

    def test_create_user_simply(self):
        user = self.manager.create_user_simply(
            email="user3@example.com", password="password"
        )
        assert user.email == "user3@example.com"
        assert user.check_password("password")

    def test_create_superuser(self):
        user = self.manager.create_superuser("superuser@example.com", "password")
        assert user.email == "superuser@example.com"
        assert user.check_password("password")
        assert user.is_staff
        assert user.is_superuser


@pytest.mark.django_db
class TestProfileModel:
    def setup(self):
        self.user1 = baker.make(Profile, email="user1@example.com")
        self.user2 = baker.make(Profile, email="user2@example.com")

    def test_follow(self):
        self.user1.follow(self.user2)
        assert self.user2 in self.user1.get_following()

    def test_unfollow(self):
        self.user1.follow(self.user2)
        self.user1.unfollow(self.user2)
        assert self.user2 not in self.user1.get_following()

    def test_get_following(self):
        self.user1.follow(self.user2)
        assert self.user2 in self.user1.get_following()

    def test_get_followers(self):
        self.user1.follow(self.user2)
        assert self.user1 in self.user2.get_followers()

    def test_get_absolute_url(self):
        assert self.user1.get_absolute_url() == reverse(
            "users:account", args=[self.user1.slug]
        )

    def test_save(self):
        self.user1.email = "newemail@example.com"
        self.user1.save()
        assert self.user1.slug == slugify(
            f"{self.user1.email.split('@')[0]}{self.user1.uuid}"
        )


@pytest.mark.django_db
def test_save_method():
    # Créer une instance de Profile avec model_bakery
    profile = baker.make(Profile, email="user@example.com")

    # Modifier l'email de l'instance
    new_email = "newemail@example.com"
    profile.email = new_email

    # Appeler la méthode save
    profile.save()

    # Vérifier que le slug a été mis à jour correctement
    expected_slug = slugify(f"{new_email.split('@')[0]}{profile.uuid}")
    assert profile.slug == expected_slug


@pytest.mark.django_db
class TestCrudProfileModel:
    def setup(self):
        self.profile = baker.make(
            Profile,
            email="user@example.com",
            username="username",
            password="password",
            year_of_birth=1990,
            season_of_birth="Spring",
            first_name="First",
            last_name="Last",
            motto="Motto",
            signature="Signature",
            about_text="About",
            continent_of_birth="AN",
            profile_picture="path/to/image.jpg",
        )
        self.profile.set_password("password")
        self.profile.save()

    def test_create_profile_with_all_fields(self):
        assert self.profile.email == "user@example.com"
        assert self.profile.username == "username"
        assert self.profile.check_password("password")
        assert self.profile.year_of_birth == 1990
        assert self.profile.season_of_birth == "Spring"
        assert self.profile.first_name == "First"
        assert self.profile.last_name == "Last"
        assert self.profile.motto == "Motto"
        assert self.profile.signature == "Signature"
        assert self.profile.about_text == "About"
        assert self.profile.continent_of_birth == "AN"
        assert self.profile.profile_picture.name == "path/to/image.jpg"

    def test_modify_profile(self):
        new_email = "newemail@example.com"
        self.profile.email = new_email
        self.profile.save()

        assert self.profile.email == new_email
        assert self.profile.slug == slugify(
            f"{new_email.split('@')[0]}{self.profile.uuid}"
        )

    def test_delete_profile(self):
        self.profile.delete()
        assert not Profile.objects.filter(email="user@example.com").exists()
