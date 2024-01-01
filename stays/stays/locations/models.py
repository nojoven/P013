import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cities_light.models import City, Country
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
from core.models import Publication

from core.utils.models_helpers import UUIDForeignKey

# Create your models here.

def uuid_generator():
    return uuid.uuid4().hex


class StayCountry(models.Model):
    uuid = models.UUIDField(default=uuid_generator, editable=False)
    publication = models.ForeignKey(
        Publication, 
        on_delete=models.CASCADE,
        null=True,
    )
    continent_name = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='continent_stay_set')
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='country_stay_set')

    def save(self, *args, **kwargs):
        if not self.country_code_of_stay:
            super().save(*args, **kwargs)
            return

        country_instance, created = Country.objects.get_or_create(code2=self.publication.country_code_of_stay)
        self.continent_name = country_instance.continent
        self.country_name = country_instance.name

        # Créer ou obtenir StayCountryHasUpvotes
        stay_country_upvotes, created = StayCountryHasUpvotes.objects.get_or_create(country_of_stay=self.country_name)

        # Incrémenter upvotes_count, que l'enregistrement existait déjà ou non
        stay_country_upvotes.upvotes_count += 1
        stay_country_upvotes.save()

        super().save(*args, **kwargs)


class StayCountryHasUpvotes(models.Model):
    country_of_stay = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
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
    country_name = models.CharField(max_length=255, null=True)
    total_upvotes = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Total upvotes cannot be negative.")]
    )

@receiver(post_save, sender=StayCountryHasUpvotes)
def update_top_upvoted_country(sender, instance, **kwargs):
    country_name = instance.country_of_stay  # Assurez-vous que le nom du pays est correctement récupéré
    country_ranking_entry, created = UpvoteCountryRanking.objects.get_or_create(country_name=country_name)

    if not created:
        # Mettez à jour la somme des upvotes_count pour ce pays
        country_ranking_entry.total_upvotes = StayCountryHasUpvotes.objects.filter(country_of_stay__name=country_name).aggregate(models.Sum('upvotes_count'))['upvotes_count__sum']
        country_ranking_entry.save()


class StayChallenge(models.Model):
    uuid = models.UUIDField(default=uuid_generator, editable=False, unique=True)
    publication_identifier = models.ForeignKey(Publication, on_delete=models.CASCADE)
    challenge_text = models.CharField(max_length=255, default="Guess where it happened :", null=True)
    is_open = models.BooleanField(default=False)
    right_answer = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    max_number_of_attempts = models.IntegerField(default=15)
    has_winner = models.BooleanField(default=False)
    winner_slug = models.ForeignKey("ChallengeAttempt", max_length=500, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    date_of_success = models.DateTimeField(null=True)
    end_date_limit = models.DateTimeField(null=True)


class ChallengeAttempt(models.Model):
    uuid = models.UUIDField(default=uuid_generator, editable=False, unique=True)
    challenge = models.ForeignKey(StayChallenge, on_delete=models.CASCADE, null=True)
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
    is_answer_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Vérifier si la réponse est correcte lors de chaque sauvegarde
        if self.answer_of_profile == self.challenge.right_answer:
            # Mettre à jour les valeurs de StayChallenge
            self.is_answer_correct = True
            self.challenge.has_winner = True
            self.challenge.is_open = False
            self.challenge.winner_slug = self.profile_of_attempt
            self.challenge.date_of_success = self.date_of_attempt
            self.challenge.end_date_limit = self.date_of_attempt

        super().save(*args, **kwargs)


class AttemptHasLocationChallenge(models.Model):
    attempt = UUIDForeignKey(ChallengeAttempt, on_delete=models.CASCADE, to_field='uuid', null=True)
    challenge = UUIDForeignKey(StayChallenge, on_delete=models.CASCADE, to_field='uuid', null=True)

    class Meta:
        unique_together = ('attempt', 'challenge')
