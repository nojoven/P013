from django.db import models

# Create your models here.
class Profile(models.Model):
    email = None
    password = None
    year_of_birth = None
    id_user = None
    detected_ip = None
    detected_continent = None
    detected_country = None
    detected_city = None
    username = None
    first_name = None
    last_name = None
    signature = None
    about_text = None
    city_of_birth = None
    country_of_birth = None
    continent_of_birth = None
    country_today = None
    citizenship_1 = None 
    citizenship_2 = None
    number_of_publications = None
    prefered_country = None
    prefered_city = None
    known_countries = None
    known_cities = None
    best_stay = None
    has_followers = None
    followers = None
    has_publications = None
    publications = None
    profile_picture = None
    background_picture = None
    followed_profiles = None
    favourite_publications = None
    motto = None
