import uuid


def uuid_generator():
    return uuid.uuid4().hex


def profile_picture_upload_to(instance, filename):
    return f"uploads/{instance.slug}/ProfilePicture/{filename}"


def build_default_username(uuid, email):
    email_parts = email.split("@")
    return f"{email_parts[0]}{uuid}{email_parts[1]}"

def retrieve_current_user(profile_email, Profile):
    current_user = Profile.objects.get(email=profile_email)
    return current_user
