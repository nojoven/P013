from django.db import models
from django_countries.fields import CountryField
from cities_light.models import City, Country, Region
# Create your models here.





class Location(models.Model):

    CONTINENTS = (
        ("AFR", "Africa"),
        ("ASI", "Asia"),
        ("EUR", "Europe"),
        ("NAM", "North America "),
        ("SAM", "South America"),
        ("OCE", "Oceania"),
    )

    given_name = models.CharField(max_length=50, unique=True, blank=False, null=True)
    category = models.ForeignKey()
    summary = models.TextField(blank=True,null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lattitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    
    continent_name = models.CharField(max_length=50, choices=CONTINENTS, blank=True, null=True)
    country = CountryField()
    city_name = models.CharField(max_length=50, blank=True, null=True)
    area_name = models.CharField(max_length=50, blank=True, null=True)
    region_name = models.CharField(max_length=50, blank=True, null=True)
    
    ranking = models.IntegerField(default=0, blank=True, null=True)
    wikipedia_url = models.URLField(default="https://lemag.ird.fr/fr", blank=True, null=True)
    interesting_data = models.TextField(blank=True,null=True)
    
    has_flag = models.BooleanField(default=False)
    flag_url = models.URLField(blank=True, null=True)
    has_map =  models.BooleanField(default=False)
    map_url = models.URLField(blank=True, null=True)
    
    celebrities_list = models.TextField(blank=True, null=True)
    has_stays = models.BooleanField(default=False)
    stays_count = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["given_name"]

class LocationCategory(models.Model):
    is_city = models.BooleanField(default=False, null=True)
    is_country = models.BooleanField(default=False, null=True)
    is_area = models.BooleanField(default=False, null=True)
    is_region = models.BooleanField(default=False, null=True)

class LocationWebData(models.Model):
    has_wiki_page = models.BooleanField(default=False)
    has_wiki_summary = models.BooleanField(default=False)
    wikipedia_url = models.URLField(default="https://lemag.ird.fr/fr", blank=True, null=True)
    wiki_summary = models.TextField(null=True)
    wiki_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    wiki_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    wiki_interesting_data = models.TextField(blank=True, null=True)
    wiki_flag_url = models.URLField(blank=True, null=True)
    wiki_map_url = models.URLField(blank=True, null=True)
    google_map_url = models.URLField(blank=True, null=True)
    wiki_celebrities_list = models.TextField(blank=True, null=True)

class LocationHasProfiles(models.Model):
    users_who_stayed = []
    users_who_upvoted = []
    location_followers = []
    location_authors = []
