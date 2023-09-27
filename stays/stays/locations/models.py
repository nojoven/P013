from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    lattitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_city = models.BooleanField
    city_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_country = models.BooleanField(default=False)
    country_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_area = models.BooleanField(default=False)
    area_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_region = models.BooleanField(default=False)
    region_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_country = models.BooleanField(default=False)
    continent_name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    ranking = models.IntegerField(default=0, blank=True, null=True)
    has_summary = models.BooleanField(default=False)
    wikipedia_url = models.URLField(default="https://lemag.ird.fr/fr", blank=True, null=True)
    summary = models.TextField(blank=True,null=True)
    interesting_data = models.TextField(blank=True,null=True)
    has_flag = models.BooleanField(default=False)
    flag_url = models.URLField(blank=True, null=True)
    has_map =  models.BooleanField(default=False)
    map_url = models.URLField(blank=True, null=True)
    celebrities_list = None
    has_stays = models.BooleanField(default=False)
    stays_count = models.IntegerField(default=0, blank=True, null=True)