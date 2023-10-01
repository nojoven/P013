from django.db import models
from math import inf

# Create your models here.
class Publication(models.Model):
    title = models.CharField(max_length=70, blank=False, null=True, help_text="Title of your publication.")
    summary = models.TextField(max_length=170, blank=False, null=True, help_text="Summarize your story.")
    date_of_post = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=5, default="text", blank=False, null=True, help_text="A text or a voice record")
    location_of_stay = models.CharField(max_length=100, blank=False, null=True)
    location_flag_url = models.URLField(null=True)
    location_map_url = models.URLField(null=True)
    image = models.URLField(null=True)
    upvotes_count = models.IntegerField(default=0, null=True)
    author_username = None
    year_of_stay = models.IntegerField(default=1950, blank=False, null=True)
    website_ranking = models.IntegerField(default=-inf, null=True)


class PublicationTypes(models.Model):
    is_text = models.BooleanField(default=True, unique=True)
    type_string_if_text = models.CharField(max_length=4, unique=True, default="text")
    is_voice = models.BooleanField(default=False, unique=True)
    type_string_if_voice = models.CharField(max_length=5, unique=True, default="voice")


    



