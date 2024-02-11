from datetime import datetime
from stays.utils.common_helpers import uuid_generator

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from locations.models import StayCountry
from core.publications_types import ContentTypes
from django_countries.fields import CountryField


def voice_story_upload_to(instance, filename):
    return f"uploads/{instance.author_slug}/{datetime.now().strftime('%Y/%m/%d')}/{instance.uuid}/voice/{filename}"

def picture_upload_to(instance, filename):
    return f"uploads/{instance.author_slug}/{datetime.now().strftime('%Y/%m/%d')}/{instance.uuid}/picture/{filename}"

def gallery_upload_to(instance, filename):
    return f"uploads/galleries/gallery/{instance.gallery.uuid}/publication/{instance.gallery.publication.uuid}/{filename}"

class PublicationType(models.Model):
    def __str__(self):
        return self.content_type

    content_type = models.CharField(max_length=5, default="text", blank=False, null=True, choices=[ContentTypes.voice.value, ContentTypes.text.value])
    is_text = models.BooleanField(default=True)
    is_voice = models.BooleanField(default=False)


# Create your models here.
class Publication(models.Model):
    def __str__(self):
        return self.title

    uuid = models.UUIDField(primary_key=True, default=uuid_generator, editable=False)
    author_username = models.CharField(blank=False, null=True, max_length=255, default=None)
    author_slug = models.SlugField(blank=False, null=True, max_length=255, default=None)
    title = models.CharField(max_length=70, blank=False, null=True, help_text="Title of your publication.")
    season_of_stay = models.CharField(max_length=6, blank=False, null=True, help_text="Title of your publication.")
    year_of_stay = models.IntegerField(default=1990, blank=False, null=True)
    summary = models.TextField(max_length=170, blank=False, null=True, help_text="Summarize your story.")
    text_story = models.TextField(max_length=25000, blank=True, null=True, help_text="Write your story.")
    voice_story = models.FileField(upload_to=voice_story_upload_to, null=False, blank=True, default=None, max_length=1000, help_text="Record your story.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=5, default="text", blank=False, null=True, choices=[ContentTypes.voice.value, ContentTypes.text.value])
    country_code_of_stay = CountryField(null=True)
    published_from_country_code = CountryField(null=True)
    picture = models.ImageField(upload_to=picture_upload_to, default="seals-6627197_1280.jpg", null=True, max_length=800)
    upvotes_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Upvotes count cannot be negative.")]
    )
    reveal_city = models.BooleanField(default=False)
    city_name = models.CharField(max_length=255, null=True)


    def get_absolute_url(self):
        return reverse('users:account', args=[self.author_slug])

# class ImageOfGallery(models.Model):
#     gallery = models.ForeignKey("core.Gallery", on_delete=models.CASCADE, null=True)
#     image = models.ImageField(upload_to=gallery_upload_to)
#     description = models.TextField(blank=True)

# class Gallery(models.Model):
#     uuid = models.UUIDField(default=uuid_generator, editable=False)
#     is_visible = models.BooleanField(default=True)
#     images = models.ManyToManyField(ImageOfGallery, related_name='gallery_images')
#     publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=True)


# class PublicationHasGallery(models.Model):
#     publication = UUIDFieldForeignKey('core.Publication', related_name='publication_galleries', on_delete=models.CASCADE, null=True)
#     gallery = UUIDFieldForeignKey('core.Gallery', related_name='gallery_publications', on_delete=models.CASCADE, null=True)

#     class Meta:
#         unique_together = ('publication', 'gallery')

class PublicationUpvote(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=True)
    upvote_profile = models.SlugField(max_length=500, null=True)
    upvote_date = models.DateTimeField(auto_now_add=True)
    upvote_value = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message="Number of attempts cannot be negative."),
            MaxValueValidator(1, message="Number of attempts cannot exceed the maximum allowed."),
        ]
    )
    class Meta:
        unique_together = (('publication', 'upvote_profile'),)


# @receiver(post_save, sender=PublicationUpvote)
# def update_upvotes_count(sender, instance, **kwargs):
#     # Incrémenter upvotes_count de la publication associée
#     if instance.publication:
#         instance.publication.upvotes_count += 1
#         instance.publication.save()
