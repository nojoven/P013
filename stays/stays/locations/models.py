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
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
from core.models import Publication

# Create your models here.

def uuid_generator():
    return uuid.uuid4().hex


class StayCountry(models.Model):
    uuid = models.UUIDField(default=uuid_generator, editable=False)
    country_code_of_stay = models.ForeignKey(Publication, on_delete=models.CASCADE, blank=True, null=True)
    continent = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='continent_stay_set')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='country_stay_set')

    def save(self, *args, **kwargs):
        if self.country_code_of_stay:
            # Obtient l'instance de Country à partir du code du pays de la publication
            country_instance = Country.objects.get(code2=self.country_code_of_stay)

            # Affecte les valeurs des clés étrangères
            self.continent = country_instance.continent
            self.country = country_instance

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.uuid)


class StayCountryHasGuess(models.Model):
    pass


class StayCountryHasUpvotes(models.Model):
    upvotes_count = models.IntegerField(default=0)


class StayCountryHasRanking(models.Model):
    pass
