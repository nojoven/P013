# signals.py
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from users.models import Profile
from icecream import ic

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, **kwargs):
    async_to_sync(update_user_status)(kwargs.get("user").email, True)

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, **kwargs):
    async_to_sync(update_user_status)(kwargs.get("user").email, False)

@database_sync_to_async
def update_user_status(user, is_online):
    try:
        profile, created = Profile.objects.get_or_create(email=user)
        profile.is_online = is_online
        profile.save()
    except Exception as e:
        ic(f"Error in update_user_status: {e}")
