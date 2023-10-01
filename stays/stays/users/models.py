from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.CharField(max_length=20, null=True, unique=True)
    email = models.EmailField(max_length=100, blank=False, null=True, help_text="Your email address", unique=True)
    password = models.CharField(max_length=50, blank=False, null=True, help_text="Your password")
    date_of_birth = models.DateField(help_text="Full user's birth date", blank=True, null=True)
    year_of_birth = models.IntegerField(help_text="User's birth year")
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=35, null=True)
    signature = models.CharField(max_length=150, null=True)
    about_text = models.TextField(max_length=20, null=True)
    city_of_birth = models.CharField(max_length=25, null=True)
    country_of_birth = models.CharField(max_length=25, null=True)
    continent_of_birth = models.CharField(max_length=15, null=True)
    country_today = models.CharField(max_length=25, null=True)
    citizenship_1 = models.CharField(max_length=25, null=True) 
    citizenship_2 = models.CharField(max_length=25, null=True)
    number_of_publications = models.IntegerField(default=0)
    prefered_country = models.CharField(max_length=25, null=True)
    prefered_city = models.CharField(max_length=25, null=True)
    prefered_continent = models.CharField(max_length=25, null=True)
    known_countries = None
    known_cities = None
    best_stay = models.CharField(max_length=255, null=True)
    has_followers = None
    followers = None
    currently_followed_profiles = None
    has_publications = None
    publications = models.IntegerField(default=0)
    profile_picture = models.URLField(null=True)
    background_picture = models.URLField(null=True)
    favourite_publications = None
    motto = models.CharField(max_length=55, null=True)
    detected_ip = models.CharField(max_length=15, null=True)
    detected_continent = models.CharField(max_length=15, null=True)
    detected_country = models.CharField(max_length=15, null=True)
    detected_city = models.CharField(max_length=20, null=True)


