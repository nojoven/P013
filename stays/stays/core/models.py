import uuid

from django.db import models
from math import inf
from core import models as core_models
from ..locations import models as location_models
from .publications_types import ContentTypes

def uuid_generator():
    return uuid.uuid4().hex

# Create your models here.
class Publication(models.Model):
    def __str__(self):
        return self.title

    uuid = models.UUIDField(default=uuid_generator, editable=False)
    author_username = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=70, blank=False, null=True, help_text="Title of your publication.")
    year_of_stay = models.IntegerField(default=1950, blank=False, null=True)
    summary = models.TextField(max_length=170, blank=False, null=True, help_text="Summarize your story.")
    date_of_post = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey('PublicationType', on_delete=models.SET_NULL, null=True)
    location_of_stay = models.CharField(max_length=100, blank=False, null=True)
    location_flag_url = models.URLField(null=True)
    location_map_url = models.URLField(null=True)
    image = models.URLField(null=True)
    upvotes_count = models.IntegerField(default=0, null=True)
    website_ranking = models.IntegerField(default=-inf, null=True)


class PublicationHasLocation(models.Model):
    publication_title = models.ForeignKey(core_models.Publication, on_delete=models.CASCADE, blank=True)
    location_given_name = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True)
    location_category = models.ForeignKey('Location', on_delete=models.CASCADE, blank=True)
    #location_exists = None
    #corresponding_location = None


class PublicationType(models.Model):
    def __str__(self):
        return self.content_type
    
    publication_title = models.ForeignKey('Publication', on_delete=models.CASCADE, blank=True)
    content_type = models.CharField(max_length=5, default="text", blank=False, null=True, choices=[ContentTypes.voice.value, ContentTypes.text.value])
    is_text = models.BooleanField(default=True)
    is_voice = models.BooleanField(default=False)
    

    

class PublicationHasProfiles(models.Model):
    publication_title = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True, null=True)
    publication_author = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True, null=True)
    publication_upvoter = models.ForeignKey('Profile', on_delete=models.CASCADE, blank=True, null=True)
    publication_upvote_count = models.IntegerField(default=0)
