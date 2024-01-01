import uuid
from django.contrib.auth import  get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from channels.db import database_sync_to_async
from django.conf import settings as dj_conf_settings
from core.models import Publication
from core.utils.models_helpers import UUIDForeignKey, SlugFieldForeignKey
from friendship.models import Follow
# from core.models import Publication

# Create your models here.


# Helper function to return uuid as string
def uuid_generator():
    return uuid.uuid4().hex

def build_default_username(uuid, email):
    email_parts = email.split("@")
    return f"{email_parts[0]}{uuid}{email_parts[1]}"

def profile_picture_upload_to(instance, filename):
    return f"uploads/{instance.slug}/ProfilePicture/{filename}"


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

    slug = models.SlugField(unique=True, blank=False, null=True, max_length=255, default=None)
    uuid = models.UUIDField(default=uuid_generator, null=True, editable=False)
    email = models.EmailField(max_length=100, blank=False, null=True, help_text="Your email address", unique=True)
    username = models.CharField(max_length=20, blank=False, null=True, unique=True)
    password = models.CharField(max_length=255, blank=False, null=True, help_text="Your password")
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
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, default="blank-profile-picture.jpg", null=True)
    # background_picture = models.ImageField(upload_to="profile_images", null=True)
    #favourite_publications = None
    # last_detected_data = models.TextField(null=True)
    #upvoted_publications_count = models

    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    def follow(self, profile):
        # Méthode pour faire en sorte que le profil actuel suive un autre profil
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
    user_profile = SlugFieldForeignKey(Profile, on_delete=models.CASCADE, null=True)
    publication_of_user = UUIDForeignKey(Publication, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('user_profile', 'publication_of_user')

class ProfileHasFollower(models.Model):
    profile_username = SlugFieldForeignKey(Profile, on_delete=models.CASCADE, null=True)
    # profile_following = models.ForeignKey('Profile.username', on_delete=models.CASCADE, blank=True)
    #profile_followers_usernames = None
    #profile_followers_count = 0







class ConnectionHistory(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    STATUS = (
        (ONLINE, 'On-line'),
        (OFFLINE, 'Off-line'),
    )
    user = models.ForeignKey(
        dj_conf_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    device_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=STATUS,
        default=ONLINE
    )
    first_login = models.DateTimeField(auto_now_add=True)
    last_echo = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "device_id"),)


    @database_sync_to_async
    def update_user_status(self, user, device_id, status):
        return ConnectionHistory.objects.get_or_create(
            user=user, device_id=device_id,
        ).update(status=status)