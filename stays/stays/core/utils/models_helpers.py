import requests
from django.db import models
from users import models as users_models
from stays.settings import NINJAS_API_KEY as napk
from icecream import ic
from django.db.models import Prefetch
from datetime import datetime
from enum import Enum


def get_publications_for_feed(publication_model, country_model, find_cities_light_country_name_with_code):
    # Fetch all publications and related upvotes
    publications = publication_model.objects.defer('picture').prefetch_related(
        Prefetch('publicationupvote_set', to_attr='upvoters')
    ).all().order_by('-created_at')

    # Fetch all countries in one query
    countries = country_model.objects.in_bulk(field_name='code2')

    for publication in publications:
        country_data = countries.get(str(publication.country_code_of_stay))

        if country_data:
            publication.stay_country_name = country_data.name
            publication.stay_continent_name = country_data.continent

        if publication.published_from_country_code:
            publication.published_from_country_name = find_cities_light_country_name_with_code(publication.published_from_country_code)
        else:
            publication.published_from_country_name = ""

        # Access the cached PublicationUpvote objects
        publication.upvoters = [upvote.upvote_profile for upvote in publication.upvoters]

    return publications


def profanity_filter_and_update(publication):
    try:
        text = publication.text_story
        headers = {'X-Api-Key': napk}
        url = 'https://api.api-ninjas.com/v1/profanityfilter?text='
        censored_text = ''
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        for chunk in chunks:
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


class ContentTypes(Enum):
    text = ("text", "text")
    voice = ("voice", "voice")


def get_profile_from_email(email: str):
    profile = users_models.Profile.objects.get(email=email)
    return profile

def get_author_picture_from_slug(author_slug: str):
    author_slug = author_slug
    author_profile = users_models.Profile.objects.get(slug=author_slug)
    return author_profile.profile_picture

def voice_story_upload_to(instance, filename):
    return f"uploads/{instance.author_slug}/{datetime.now().strftime('%Y/%m/%d')}/{instance.uuid}/voice/{filename}"

def picture_upload_to(instance, filename):
    return f"uploads/{instance.author_slug}/{datetime.now().strftime('%Y/%m/%d')}/{instance.uuid}/picture/{filename}"
