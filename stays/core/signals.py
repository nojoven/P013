from cities_light.models import Country
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Publication, PublicationUpvote
from locations.models import StayCountry
from users.models import Profile, ProfileHasPublication


@receiver(post_save, sender=Publication)
def create_stay_country(sender, instance, created, **kwargs):
    # Vérifier si country_code_of_stay de la Publication existe déjà dans Country.code2
    if (
        created
        and Country.objects.filter(code2=instance.country_code_of_stay).exists()
        and not StayCountry.objects.filter(
            country_code_of_stay=instance.country_code_of_stay
        ).exists()
    ):
        # Si le country_code_of_stay existe, obtenir les informations du pays
        country_instance = Country.objects.get(code2=instance.country_code_of_stay)
        # Créer une nouvelle instance de StayCountry
        StayCountry.objects.create(
            publication=instance,
            country_code_of_stay=instance.country_code_of_stay,
            continent_name=country_instance.continent,
            country_name=country_instance.name,
        )


@receiver(post_save, sender=PublicationUpvote)
def update_upvotes_count(sender, instance, created, **kwargs):
    # Incrémenter upvotes_count de la publication associée
    if created and instance.publication:
        instance.publication.upvotes_count += 1
        instance.publication.save()


@receiver(post_save, sender=Publication)
def create_profile_has_publication(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.get(slug=instance.author_slug)
        ProfileHasPublication.objects.create(
            publication_of_user=instance, user_profile=user_profile
        )
