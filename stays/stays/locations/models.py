import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from cities_light.models import City, Country
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
from core.models import Publication
from users.models import Profile

from core.utils.models_helpers import SlugFieldForeignKey, UUIDFieldForeignKey, NullableBigIntegerFieldForeignKey

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
    continent_name = models.CharField(null=True)
    country_name = models.CharField(null=True)
    country_code_of_stay = CountryField(null=True)

    # def save(self, *args, **kwargs):
    #     if not self.country_code_of_stay:
    #         super().save(*args, **kwargs)
    #         return

    #     country_instance, created = Country.objects.get_or_create(code2=self.publication.country_code_of_stay)
    #     self.continent_name = country_instance.continent
    #     self.country_name = country_instance.name

    #     # Créer ou obtenir StayCountryHasUpvotes
    #     stay_country_upvotes, created = StayCountryHasUpvotes.objects.get_or_create(country_of_stay=self.country_name)

    #     # Incrémenter upvotes_count, que l'enregistrement existait déjà ou non
    #     stay_country_upvotes.upvotes_count += 1
    #     stay_country_upvotes.save()

    #     super().save(*args, **kwargs)


# class StayCountryHasUpvotes(models.Model):
#     country_of_stay = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
#     upvotes_count = models.IntegerField(
#         default=0,
#         validators=[MinValueValidator(0, message="Upvotes count cannot be negative.")]
#     )


# class UpvoteCountryRanking(models.Model):
#     country_name = models.CharField(max_length=255, null=True)
#     total_upvotes = models.IntegerField(
#         default=0,
#         validators=[MinValueValidator(0, message="Total upvotes cannot be negative.")]
#     )


# class StayChallenge(models.Model):
#     uuid = models.UUIDField(default=uuid_generator, editable=False)
#     publication_identifier = models.ForeignKey(Publication, on_delete=models.CASCADE)
#     challenge_text = models.CharField(max_length=255, default="Guess where it happened :", null=True)
#     is_open = models.BooleanField(default=False)
#     right_answer = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
#     max_number_of_attempts = models.IntegerField(default=5)
#     has_winner = models.BooleanField(default=False)
#     winner_slug = models.SlugField(max_length=500, null=True)
#     start_date = models.DateTimeField(null=True)
#     date_of_success = models.DateTimeField(null=True)
#     end_date_limit = models.DateTimeField(null=True)


# class ChallengeAttempt(models.Model):
#     uuid = models.UUIDField(default=uuid_generator, editable=False)
#     challenge = models.ForeignKey(StayChallenge, on_delete=models.CASCADE, null=True)
#     profile_of_attempt = SlugFieldForeignKey(Profile, max_length=500, null=True, on_delete=models.CASCADE, to_field="slug")
#     date_of_attempt = models.DateTimeField(auto_now_add=True)
#     incrementation_number = models.IntegerField(default=1)
#     number_of_attempts = models.IntegerField(
#         default=0,
#         validators=[
#             MinValueValidator(0, message="Number of attempts cannot be negative."),
#             MaxValueValidator(1, message="Number of attempts cannot exceed the maximum allowed."),
#         ]
#     )
#     answer_of_profile = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
#     is_answer_correct = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         # Vérifier si la réponse est correcte lors de chaque sauvegarde
#         if self.answer_of_profile == self.challenge.right_answer:
#             # Mettre à jour les valeurs de StayChallenge
#             self.is_answer_correct = True
#             self.challenge.has_winner = True
#             self.challenge.is_open = False
#             self.challenge.winner_slug = self.profile_of_attempt
#             self.challenge.date_of_success = self.date_of_attempt
#             self.challenge.end_date_limit = self.date_of_attempt

#             # Update ProfileRemainingAttempts
#             remaining_attempts_instance, _ = ProfileRemainingAttempts.objects.get_or_create(
#                 challenge_id=self.challenge_id,
#                 profile_slug=self.profile_of_attempt.slug,
#                 defaults={'remaining_attempts': self.challenge.max_number_of_attempts}
#             )

#             ProfileRemainingAttempts.objects.filter(
#                 challenge_id=self.challenge_id,
#                 profile_slug=self.profile_of_attempt.slug
#             ).update(
#                 remaining_attempts=models.F('remaining_attempts') - 1
#             )

#         super().save(*args, **kwargs)


# class AttemptHasLocationChallenge(models.Model):
#     attempt = models.ForeignKey(ChallengeAttempt, on_delete=models.CASCADE, to_field='id', null=True)
#     challenge = models.ForeignKey(StayChallenge, on_delete=models.CASCADE, to_field='id', null=True)

#     class Meta:
#         unique_together = ('attempt', 'challenge')

# class ProfileRemainingAttempts(models.Model):
#     challenge_id = NullableBigIntegerFieldForeignKey(StayChallenge, on_delete=models.CASCADE, to_field='id', null=True)
#     profile_slug = SlugFieldForeignKey(Profile, on_delete=models.CASCADE, to_field='slug', null=True)
#     remaining_attempts = models.IntegerField(default=5)
