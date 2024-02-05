import requests
from django.db import models
from users import models as users_models
from stays.settings import NINJAS_API_KEY as napk
from icecream import ic

def profanity_filter_and_update(publication):
    try:
        text = publication.text_story
        headers = {'X-Api-Key': napk}
        url = 'https://api.api-ninjas.com/v1/profanityfilter?text='
        censored_text = ''
        for i in range(0, len(text), 1000):
            chunk = text[i:i+1000]
            response = requests.get(url + chunk, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            if data['has_profanity']:
                censored_text += data['censored']
            else:
                censored_text += data['original']
        if censored_text != text:
            publication.text_story = censored_text
            publication.save()
    except requests.exceptions.RequestException as e:
        ic(f"Request to profanity filter API failed: {e}")
    except Exception as e:
        ic(f"Unexpected error in profanity_filter_and_update: {e}")


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
    profile = users_models.Profile.objects.get(email=email)
    return profile

def get_author_picture_from_slug(author_slug: str):
    author_slug = author_slug
    author_profile = users_models.Profile.objects.get(slug=author_slug)
    return author_profile.profile_picture
