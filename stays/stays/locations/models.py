import uuid

from django.db import models
from django_countries.fields import CountryField
from cities_light.settings import ICity, ISubRegion, IRegion, ICountry
from cities_light.models import City, Country, Region
from cities_light.abstract_models import (
    AbstractSubRegion,
    AbstractCity,
    AbstractRegion,
    AbstractCountry)
from cities_light.receivers import connect_default_signals
# Create your models here.


def uuid_generator():
    return uuid.uuid4().hex


class CountryRecord(AbstractCountry):
    pass
#connect_default_signals(Country)


class RegionRecord(AbstractRegion):
    pass
#connect_default_signals(Region)


class RegionRecord(AbstractSubRegion):
    pass
# connect_default_signals(SubRegion)


class CityRecord(AbstractCity):
    timezone = models.CharField(max_length=40)
# connect_default_signals(City)


class ContinentHasPublication(models.Model):
    continent_code = models.CharField(max_length=2, primary_key=True, unique=True)
    pass


class ContinentHasCountry(models.Model):
    continent_code = models.CharField(max_length=2, primary_key=True, unique=True)
    pass


class CountryHasPublication(models.Model):
    pass


class CountryHasCity(models.Model):
    pass


class CountryHasRegion(models.Model):
    pass


class RegionHasPublication(models.Model):
    pass


class RegionHasCity(models.Model):
    pass


class RegionHasSubregion(models.Model):
    pass


class SubRegionHasCity(models.Model):
    pass


class SubRegionHasPublication(models.Model):
    pass


class CityHasPublication(models.Model):
    pass


class LocationCategory(models.Model):

    def __str__(self):
        return self.category

    # location_given_name = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True)
    is_city = models.BooleanField(default=False, null=True)
    is_country = models.BooleanField(default=False, null=True)
    is_area = models.BooleanField(default=False, null=True)
    is_region = models.BooleanField(default=False, null=True)

    if is_city is True:
        category = "city"
    elif is_country is True:
        category = "country"
    elif is_area is True:
        category = "area"
    elif is_region is True:
        category = "region"
    else:
        category = "unknown"


class LocationRecord(models.Model):

    CONTINENTS = (
        ("AFR", "Africa"),
        ("ASI", "Asia"),
        ("EUR", "Europe"),
        ("NAM", "North America "),
        ("SAM", "South America"),
        ("OCE", "Oceania"),
    )

    def __str__(self):
        return self.given_name

    uuid = models.UUIDField(default=uuid_generator, editable=False)
    # location_given_name = models.CharField(max_length=50, unique=True, blank=False, null=True)
    # location_category = models.ForeignKey(LocationCategory, on_delete=models.CASCADE, blank=True)
    # summary = models.TextField(blank=True,null=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # lattitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)

    # continent_name = models.CharField(max_length=50, choices=CONTINENTS, blank=True, null=True)
    country = CountryField()
    # city_name = models.CharField(max_length=50, blank=True, null=True)
    # area_name = models.CharField(max_length=50, blank=True, null=True)
    # region_name = models.CharField(max_length=50, blank=True, null=True)

    ranking = models.IntegerField(default=0, blank=True, null=True)

    has_stays = models.BooleanField(default=False)
    stays_count = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ["ranking"]


class LocationWebData(models.Model):
    location_given_name = models.ForeignKey(LocationRecord, on_delete=models.CASCADE, blank=True,)
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


class LocationHasProfileActivity(models.Model):
    location_given_name = models.ForeignKey(LocationRecord, on_delete=models.CASCADE, blank=True)
    # user_who_stayed = models.ForeignKey('Profile.username', on_delete=models.CASCADE, blank=True)
    # user_who_upvoted = models.ForeignKey('Profile.username', on_delete=models.CASCADE, blank=True)
    # location_followers = []
    # location_author = []
    location_upvotes_count = models.IntegerField(default=0)
