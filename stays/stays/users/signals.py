# signals.py
from channels.db import database_sync_to_async
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import ConnectionStatus, Profile

@receiver(user_logged_in)
async def user_logged_in_handler(sender, request, **kwargs):
    profile = Profile.objects.get(user=request.user)
    profile.is_online = True
    profile.save()
    await update_user_status(profile, True)

@receiver(user_logged_out)
async def user_logged_out_handler(sender, request, **kwargs):
    profile = Profile.objects.get(user=request.user)
    profile.is_online = False
    profile.save()
    await update_user_status(profile, False)

@database_sync_to_async
def update_user_status(profile, is_online):
    ConnectionStatus.objects.update_or_create(
        profile=profile,
        is_online=is_online
    )
