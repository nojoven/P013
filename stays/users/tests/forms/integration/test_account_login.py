import re

from django.urls import reverse
from django_webtest import WebTest
from model_bakery import baker


class TestAccountLoginForm(WebTest):
    csrf_checks = False

    def setUp(self):
        # Créez des instances de modèles nécessaires pour les tests ici
        self.user = baker.make("users.Profile", email="testuser@example.com")
        self.user.set_password("password")  # Définissez le mot de passe en clair
        self.user.save()

    def test_form_valid(self):
        # Préparez les données du formulaire
        form_data = {
            "email": "testuser@example.com",
            "password": "password",
        }

        # Simulez une requête POST sur la vue de connexion
        response = self.app.post(reverse("users:login"), params=form_data)

        # Vérifiez que la réponse est correcte
        self.assertEqual(response.status_code, 200)

    def test_form_no_email(self):
        # Préparez les données du formulaire
        form_data = {
            "password": "password",
        }

        # Simulez une requête POST sur la vue de connexion
        response = self.app.post(reverse("users:login"), params=form_data)
        # Utilisez une expression régulière pour extraire le titre de la page
        match = re.search("<title>(.*?)</title>", response.text)

        # Vérifiez que le titre de la page est toujours "Sign In"
        if match:
            title = match.group(1)
            self.assertEqual(title, "sign in")

    def test_form_no_password(self):
        # Préparez les données du formulaire
        form_data = {
            "email": "testuser@example.com",
        }

        # Simulez une requête POST sur la vue de connexion
        response = self.app.post(reverse("users:login"), params=form_data)
        # Utilisez une expression régulière pour extraire le titre de la page
        match = re.search("<title>(.*?)</title>", response.text)

        # Vérifiez que le titre de la page est toujours "Sign In"
        if match:
            title = match.group(1)
            self.assertEqual(title, "sign in")
