import uuid
from django.contrib.auth import  get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse

# from core.models import Publication

# Create your models here.


# Helper function to return uuid as string
def uuid_generator():
    return uuid.uuid4().hex

def build_default_username(uuid, email):
    email_parts = email.split("@")
    return f"{email_parts[0]}{uuid}{email_parts[1]}"

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

    SEASONS = (("Spring", 1), ("Summer", 2), ("Autumn", 3), ("Winter", 4),) 

    uuid = models.UUIDField(default=uuid_generator, null=True, editable=False)
    email = models.EmailField(max_length=100, blank=False, null=True, help_text="Your email address", unique=True)
    username = models.CharField(max_length=20, blank=False, null=True, unique=True)
    password = models.CharField(max_length=255, blank=False, null=True, help_text="Your password")
    # date_of_birth = models.DateField(help_text="Full user's birth date", blank=True, null=True)
    year_of_birth = models.IntegerField(help_text="User's birth year", default=1900, null=False)
    season_of_birth = models.CharField(max_length=50, default="Spring", blank=False, null=False)
    first_name = models.CharField(max_length=25, blank=False, null=True)
    last_name = models.CharField(max_length=35, blank=False, null=True)
    motto = models.CharField(max_length=100, blank=False, null=False, default="I LOVE THIS WEBSITE!")
    signature = models.CharField(max_length=150, blank=False, null=True, unique=True)
    about_text = models.TextField(blank=False, null=True, default="Once upon a time...")
    # city_of_birth = models.CharField(max_length=25, null=True)
    # country_of_birth = models.CharField(max_length=25, null=True)
    # continent_of_birth = models.CharField(max_length=15, null=True)
    # country_today = models.CharField(max_length=25, null=True)
    # citizenship_1 = models.CharField(max_length=25, null=True) 
    # citizenship_2 = models.CharField(max_length=25, null=True)
    # number_of_publications = models.IntegerField(default=0)
    # prefered_country = models.CharField(max_length=25, null=True)
    # prefered_city = models.CharField(max_length=25, null=True)
    # prefered_continent = models.CharField(max_length=25, null=True)
    # known_countries = None
    # known_cities = None
    # best_stay = models.CharField(max_length=255, null=True)
    # has_followers = None
    # followers = models.ManyToManyField("self", symmetrical=False)
    # profile_follows = models.ManyToManyField(User, related_name="followers")
    #has_publications = None
    # publications =  models.ManyToManyField(Publication, related_name="author") 
    profile_picture = models.ImageField(upload_to="profile_images", default="blank-profile-picture.jpg", null=True)
    # background_picture = models.ImageField(upload_to="profile_images", null=True)
    #favourite_publications = None
    # last_detected_data = models.TextField(null=True)
    #upvoted_publications_count = models

    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    # def get_absolute_url(self):
    #     return reverse("profile-detail", kwargs={"pk": self.pk})

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



class ProfileFollowers(models.Model):
    profile_username = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    # profile_following = models.ForeignKey('Profile.username', on_delete=models.CASCADE, blank=True)
    #profile_followers_usernames = None
    #profile_followers_count = 0

class ProfileHasDetectedData(models.Model):
    connected_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    last_detected_ip = models.CharField(max_length=15, null=True)
    last_detected_continent = models.CharField(max_length=15, null=True)
    last_detected_country = models.CharField(max_length=15, null=True)
    last_detected_city = models.CharField(max_length=20, null=True)
