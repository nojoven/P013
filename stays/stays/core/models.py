import os
import uuid
import sys
from pathlib import Path

#sys.path.append(Path(os.getcwd()).parent.parent.absolute)

from django.db import models
from math import inf
from users.models import Profile
from locations.models import Location
from core.publications_types import ContentTypes



def uuid_generator():
    return uuid.uuid4().hex

class PublicationType(models.Model):
    def __str__(self):
        return self.content_type
    
    # publication_title = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True)
    content_type = models.CharField(max_length=5, default="text", blank=False, null=True, choices=[ContentTypes.voice.value, ContentTypes.text.value])
    is_text = models.BooleanField(default=True)
    is_voice = models.BooleanField(default=False)


# Create your models here.
class Publication(models.Model):
    def __str__(self):
        return self.title
    
    uuid = models.UUIDField(primary_key=True, default=uuid_generator, editable=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=70, blank=False, null=True, help_text="Title of your publication.")
    year_of_stay = models.IntegerField(default=1950, blank=False, null=True)
    summary = models.TextField(max_length=170, blank=False, null=True, help_text="Summarize your story.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(PublicationType, on_delete=models.SET_NULL, null=True)
    location_of_stay = models.CharField(max_length=100, blank=False, null=True)
    location_flag_url = models.URLField(null=True)
    location_map_url = models.URLField(null=True)
    image = models.URLField(null=True)
    upvotes_count = models.IntegerField(default=0, null=True)
    website_ranking = models.IntegerField(default=-inf, null=True)


class PublicationHasLocation(models.Model):
    publication_title = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True)
    given_name = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, related_name="given_name")
    category = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, related_name="category")
    #location_exists = None
    #corresponding_location = None


class PublicationHasProfiles(models.Model):
    publication_title = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name="title")
    publication_author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    publication_upvoter = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name="upvote_count")
    publication_upvote_count = models.IntegerField(default=0)
