import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from cities_light.settings import ICity, ISubRegion, IRegion, ICountry
from cities_light.models import City, Country, Region
from cities_light.abstract_models import (
    AbstractSubRegion,
    AbstractCity,
    AbstractRegion,
    AbstractCountry)
from cities_light.receivers import connect_default_signals
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
from core.models import Publication
from users.models import Profile

# Create your models here.

def uuid_generator():
    return uuid.uuid4().hex


class StayCountry(models.Model):
    uuid = models.UUIDField(default=uuid_generator, editable=False)
    country_code_of_stay = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    continent_name = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='continent_stay_set')
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='country_stay_set')

    def save(self, *args, **kwargs):
        if self.country_code_of_stay:
            country_instance = Country.objects.get(code2=self.country_code_of_stay)
            self.continent_name = country_instance.continent
            self.country_name = country_instance.name

            # Créer ou mettre à jour StayCountryHasUpvotes
            stay_country_upvotes, created = StayCountryHasUpvotes.objects.get_or_create(country_of_stay=self.country_name)
            if not created:
                stay_country_upvotes.upvotes_count += 1
                stay_country_upvotes.save()

        super().save(*args, **kwargs)


class StayCountryHasUpvotes(models.Model):
    country_of_stay = models.ForeignKey(Country, on_delete=models.CASCADE)
    upvotes_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Upvotes count cannot be negative.")]
    )


# Signal pour mettre à jour StayCountryHasUpvotes après chaque sauvegarde de StayCountry
@receiver(post_save, sender=StayCountry)
def update_upvotes_count(sender, instance, **kwargs):
    stay_country_upvotes, created = StayCountryHasUpvotes.objects.get_or_create(country_of_stay=instance.country_name)
    if not created:
        stay_country_upvotes.upvotes_count += 1
        stay_country_upvotes.save()



class UpvoteCountryRanking(models.Model):
    country_name = models.CharField(max_length=255, unique=True)
    total_upvotes = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Total upvotes cannot be negative.")]
    )

@receiver(post_save, sender=StayCountryHasUpvotes)
def update_top_upvoted_country(sender, instance, **kwargs):
    country_name = instance.country_of_stay  # Assurez-vous que le nom du pays est correctement récupéré
    top_country, created = UpvoteCountryRanking.objects.get_or_create(country_name=country_name)

    if not created:
        # Mettez à jour la somme des upvotes_count pour ce pays
        top_country.total_upvotes = StayCountryHasUpvotes.objects.filter(country_of_stay__name=country_name).aggregate(models.Sum('upvotes_count'))['upvotes_count__sum']
        top_country.save()


class StayChallenge(models.Model):
    pass
    publication_identifier = models.ForeignKey(Publication, on_delete=models.CASCADE)
    challenge_text = models.CharField(max_length=255, default="Guess where it happened :", null=True)
    is_open = models.BooleanField(default=False)
    right_answer = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    max_number_of_attempts = models.IntegerField(default=15)
    has_winner = models.BooleanField(default=False)
    winner_slug = models.ForeignKey("ChallengeAttempt", max_length=500, null=True, on_delete=models.CASCADE)


class ChallengeAttempt(models.Model):
    pass
    challenge_identifier = models.ForeignKey(StayChallenge, on_delete=models.CASCADE, null=True)
    profile_of_attempt = models.SlugField(max_length=500, null=True)
    date_of_attempt = models.DateTimeField(auto_now_add=True)
    number_of_attempts = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message="Number of attempts cannot be negative."),
            MaxValueValidator(15, message="Number of attempts cannot exceed the maximum allowed."),
        ]
    )
    answer_of_profile = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

