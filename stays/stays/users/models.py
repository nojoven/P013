from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from channels.db import database_sync_to_async
from django.contrib.auth import  get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from channels.db import database_sync_to_async
from django.conf import settings as dj_conf_settings
from core.models import Publication
from core.utils.models_helpers import UUIDFieldForeignKey, SlugFieldForeignKey, BooleanFieldForeignKey
from friendship.models import Follow
from cities_light.models import CONTINENT_CHOICES, Country, City
from django_countries.fields import CountryField
# from core.models import Publication
from users.utils import uuid_generator, profile_picture_upload_to, build_default_username

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")

        # Lower the domain part of the email address before creating the user
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user_simply(**params):
        """Helper function to create new user"""
        return get_user_model().objects.create_user(**params)

    def create_superuser(self, email, password=None):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    is_online = models.BooleanField(default=False, verbose_name="Online Status")
    slug = models.SlugField(unique=True, blank=False, null=True, max_length=255, default=None)
    uuid = models.UUIDField(default=uuid_generator, null=True, editable=False)
    email = models.EmailField(max_length=100, blank=False, null=True, help_text="Your email address", unique=True)
    username = models.CharField(max_length=44, blank=False, null=True, unique=True)
    password = models.CharField(max_length=255, blank=False, null=True, help_text="Your password")
    year_of_birth = models.IntegerField(help_text="User's birth year", default=1900, null=False)
    season_of_birth = models.CharField(max_length=50, default="Spring", blank=False, null=False)
    first_name = models.CharField(max_length=25, blank=False, null=True)
    last_name = models.CharField(max_length=35, blank=False, null=True)
    motto = models.CharField(max_length=100, blank=False, null=False, default="I LOVE THIS WEBSITE!")
    signature = models.CharField(max_length=150, blank=False, null=True, unique=True)
    about_text = models.TextField(blank=False, null=True, default="Once upon a time...")
    continent_of_birth = models.CharField(max_length=15, choices=CONTINENT_CHOICES, null=True, default='AN')
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, default="blank-profile-picture.jpg", null=True)
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    def follow(self, profile):
        # Méthode pour faire en sorte que le profil actuel suive un autre profile
        Follow.objects.add_follower(self, profile)

    def unfollow(self, profile):
        # Méthode pour faire en sorte que le profil actuel cesse de suivre un autre profil
        Follow.objects.remove_follower(self, profile)

    def get_following(self):
        # Méthode pour récupérer les profils suivis par le profil actuel
        return Follow.objects.following(self)

    def get_followers(self):
        # Méthode pour récupérer les profils qui suivent le profil actuel
        return Follow.objects.followers(self)

    def get_absolute_url(self):
        return reverse('users:account', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.email.split('@')[0]}{self.uuid}")
        super().save(*args, **kwargs)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class ProfileHasPublication(models.Model):
    user_profile = SlugFieldForeignKey(Profile, to_field='slug', on_delete=models.CASCADE, null=True)
    publication_of_user = UUIDFieldForeignKey(Publication, to_field='uuid', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('user_profile', 'publication_of_user')
