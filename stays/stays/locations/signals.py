from django.db.models.signals import post_save
from django.dispatch import receiver
# from locations.models import StayCountry, StayCountryHasUpvotes, UpvoteCountryRanking


# # Signal pour mettre à jour StayCountryHasUpvotes après chaque sauvegarde de StayCountry
# @receiver(post_save, sender=StayCountry)
# def update_upvotes_count(sender, instance, **kwargs):
#     stay_country_upvotes, created = StayCountryHasUpvotes.objects.get_or_create(country_of_stay=instance.country_name)
#     if not created:
#         stay_country_upvotes.upvotes_count += 1
#         stay_country_upvotes.save()


# @receiver(post_save, sender=StayCountryHasUpvotes)
# def update_top_upvoted_country(sender, instance, **kwargs):
#     country_name = instance.country_of_stay  # Assurez-vous que le nom du pays est correctement récupéré
#     country_ranking_entry, created = UpvoteCountryRanking.objects.get_or_create(country_name=country_name)

#     if not created:
#         # Mettez à jour la somme des upvotes_count pour ce pays
#         country_ranking_entry.total_upvotes = StayCountryHasUpvotes.objects.filter(country_of_stay__name=country_name).aggregate(models.Sum('upvotes_count'))['upvotes_count__sum']
#         country_ranking_entry.save()