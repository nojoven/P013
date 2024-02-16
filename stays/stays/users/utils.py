from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

def profile_picture_upload_to(instance, filename):
    return f"uploads/{instance.slug}/ProfilePicture/{filename}"


def build_default_username(uuid, email):
    email_parts = email.split("@")
    return f"{email_parts[0]}{uuid}{email_parts[1]}"

def retrieve_current_user(profile_email, Profile):
    return Profile.objects.get(email=profile_email)

def get_email_to_user(form):
    # Vérifiez que l'utilisateur a été correctement récupéré
    if next(form.get_users(form.email_to), None) is None:
        raise ValueError(f"No user found with email {form.email_to}")

    return next(form.get_users(form.email_to))

def forge_token(user):
    return default_token_generator.make_token(user)

def generate_reset_uid(pk):
    return urlsafe_base64_encode(force_bytes(pk))

def generate_recovery_url(request, uid, token):
    return request.build_absolute_uri(reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

