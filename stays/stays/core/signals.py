from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import PublicationUpvote

@receiver(post_save, sender=PublicationUpvote)
def update_upvotes_count(sender, instance, **kwargs):
    # Incrémenter upvotes_count de la publication associée
    if instance.publication:
        instance.publication.upvotes_count += 1
        instance.publication.save()

