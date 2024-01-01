# signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from channels.db import database_sync_to_async
from users.models import ConnectionHistory, Profile

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # Utilisateur connecté
    profile = Profile.objects.get(user=user)  # Adapté selon votre relation entre User et Profile
    update_user_status(profile, profile.device_id, ConnectionHistory.ONLINE)

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    # Utilisateur déconnecté
    profile = Profile.objects.get(user=user)  # Adapté selon votre relation entre User et Profile
    update_user_status(profile, profile.device_id, ConnectionHistory.OFFLINE)

@database_sync_to_async
def update_user_status(profile, device_id, status):
    # Mettez à jour l'état de connexion du profil
    profile.is_online = (status == ConnectionHistory.ONLINE)
    profile.save()

    # Mettez à jour l'historique de connexion
    return ConnectionHistory.objects.get_or_create(
        profile=profile, device_id=device_id,
    ).update(status=status)