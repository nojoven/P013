from django.db import models
from users import models as users_models


class UUIDFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)


class CharFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['max_length'] = kwargs.get('max_length', 500)
        super().__init__(to, **kwargs)


class SlugFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(to, **kwargs)


class NullableIntegerFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)


class NullableBigIntegerFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)


class BooleanFieldForeignKey(models.ForeignKey):
    def __init__(self, to, **kwargs):
        kwargs['db_column'] = kwargs.get('db_column', None)
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(to, **kwargs)


def get_all_profiles():
    profiles = users_models.Profile.objects.all()
    return profiles


def get_profile_from_email(email: str):
    profile = Profile.objects.get(email=email)
    return profile

def get_author_picture_from_slug(author_slug: str):
    author_slug = author_slug
    author_profile = Profile.objects.get(slug=author_slug)
    return author_profile.profile_picture
