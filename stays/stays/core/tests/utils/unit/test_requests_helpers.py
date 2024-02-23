# Importations nécessaires pour les tests
from django.http import HttpResponse
from django.test import RequestFactory
from django.views import View
from core.utils.requests_helpers import NeverCacheMixin
from icecream import ic


# Création d'une vue de test qui utilise NeverCacheMixin
class TestView(NeverCacheMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse()

# Test de NeverCacheMixin
def test_never_cache_mixin():
    # Création d'une instance de RequestFactory
    factory = RequestFactory()

    # Création d'une requête GET
    request = factory.get('/')

    # Création d'une instance de TestView
    view = TestView.as_view()

    # Appel de la méthode dispatch de la vue avec la requête
    response = view(request)
    ic(response)
    ic(response['Cache-Control'])

    # Vérification que la réponse a l'en-tête 'Cache-Control' défini sur 'max-age, no-cache, no-store, must-revalidate'
    assert response['Cache-Control'] == 'max-age=0, no-cache, no-store, must-revalidate, private'