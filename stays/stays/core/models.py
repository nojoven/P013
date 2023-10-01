from django.db import models
from math import inf
from .publications_types import ContentTypes

# Create your models here.
class Publication(models.Model):
    author_username = None
    title = models.CharField(max_length=70, blank=False, null=True, help_text="Title of your publication.")
    year_of_stay = models.IntegerField(default=1950, blank=False, null=True)
    summary = models.TextField(max_length=170, blank=False, null=True, help_text="Summarize your story.")
    date_of_post = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey()
    location_of_stay = models.CharField(max_length=100, blank=False, null=True)
    location_flag_url = models.URLField(null=True)
    location_map_url = models.URLField(null=True)
    image = models.URLField(null=True)
    upvotes_count = models.IntegerField(default=0, null=True)
    website_ranking = models.IntegerField(default=-inf, null=True)


class PublicationHasLocation(models.Model):
    publication_location_given_name = None
    publication_location_category = None
    location_exists = None
    corresponding_location = None

class PublicationHasType(models.Model):
    publication_title = None
    publication_type = None
    publication_is_text = None
    publication_is_voice = None

class PublicationTypes(models.Model):
    is_text = models.BooleanField(default=True, unique=True)
    is_voice = models.BooleanField(default=False, unique=True)
    content_type = models.CharField(max_length=5, default="text", blank=False, null=True, choices=[ContentTypes.voice, ContentTypes.text])


class PublicationHasProfiles(models.Model):
    publication_title = None
    publication_author = None
    publication_upvoters = []
    publication_upvote_count = 0
