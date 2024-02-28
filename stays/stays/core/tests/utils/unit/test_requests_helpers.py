# Importations nécessaires pour les tests
from django.http import HttpResponse
from django.test import RequestFactory
from django.views import View
from core.utils.requests_helpers import NeverCacheMixin, get_cache_key
from icecream import ic
from django.test import TestCase
from django.core.cache import cache
from core.models import Publication
from model_bakery import baker
from stays.utils.common_helpers import uuid_generator
from users.models import Profile
from cities_light.models import Country
from uuid import uuid4
from datetime import datetime
import random
from core.utils.models_helpers import ContentTypes
from django.test import Client
from django.urls import reverse


# Création d'une vue de test qui utilise NeverCacheMixin
class TestView(NeverCacheMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse()

# Test de NeverCacheMixin
class TestNeverCacheMixin(TestCase):
    def test_never_cache_mixin(self):
        factory = RequestFactory()
        request = factory.get('/')
        view = TestView.as_view()
        response = view(request)
        self.assertEqual(response['Cache-Control'], 'max-age=0, no-cache, no-store, must-revalidate, private')


class TestGetCacheKey(TestCase):
    def setUp(self):
        self.profile = baker.make(Profile,
            email='testadmin@example.com',
            slug = f"testadmin{uuid_generator()}",
            username = 'testadmin',
            profile_picture = 'picture.jpg'
        )
        self.profile.set_password('testpasYEF93*&5sword')
        self.profile.save()

        # Création d'une instance de Country
        self.country = Country.objects.create(name='France', code2='FR')
        # Create some instances of the model
        self.words = [
            'Full', 'Story', 'Test', 'Publication', 'Voice', 'Audio', 'Home', 'View'
            'apple', 'banana', 'cherry', 'date', 'elderberry',
            'fig', 'grape', 'honeydew', 'iceberg', 'jackfruit',
            'kiwi', 'lemon', 'mango', 'nectarine', 'orange',
            'pineapple', 'quince', 'raspberry', 'strawberry', 'tangerine',
            'ugli', 'vanilla', 'watermelon', 'xigua', 'yellow'
        ]
        # Création de plusieurs instances de Publication
        for need in range(12):
            Publication.objects.create(
        
                uuid = uuid4(),
                title=' '.join(random.choices(self.words, k=3)), 
                author_username=self.profile.username, 
                author_slug=self.profile.slug, 
                # picture='picture.jpg',
                text_story='This is a full story.',
                content_type=ContentTypes.text.value[0],
                season_of_stay='Winter',
                year_of_stay=2000,
                summary='This is a summary.',
                created_at=datetime.now(),
                country_code_of_stay=self.country.code2,
                published_from_country_code="FR",
                upvotes_count=0
            )
            self.publications = Publication.objects.all()
            # Création d'un client de test
            self.client = Client(enforce_csrf_checks=False)
            self.url = reverse('core:home')

    def test_get_cache_key(self):
        # Get the function from get_cache_key
        _get_cache_key = get_cache_key(Publication)

        # Check that the cache is initially empty
        self.assertIsNotNone(cache.get('publications_count'))

        # Call _get_cache_key and check the returned key
        key = _get_cache_key()
        self.assertTrue(len(key) > len('home_page_'))
