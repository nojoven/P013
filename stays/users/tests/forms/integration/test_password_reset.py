from model_bakery import baker
from django.test import TestCase
from users.forms import PasswordResetForm
from django.utils import timezone
from django.test import Client
from django.test.client import RequestFactory
from stays.settings import (
    EMAIL_HOST_USER,
    MAILGUN_API_KEY,
    MAILGUN_DOMAIN_NAME,
    DEFAULT_EMAIL_DESTINATION,
)


class TestPasswordResetForm(TestCase):
    def setUp(self):
        # Créez des instances de modèles nécessaires pour les tests ici
        self.user = baker.make(
            "users.Profile", email=DEFAULT_EMAIL_DESTINATION, password="password"
        )
        self.user.last_login = timezone.now()
        self.user.save()

        # Simulez une première connexion de l'utilisateur
        self.client = Client()
        self.client.login(email=DEFAULT_EMAIL_DESTINATION, password="password")

        # Créez un objet request factice
        self.factory = RequestFactory()

    def test_sending_values(self):
        assert all(
            (
                EMAIL_HOST_USER,
                MAILGUN_API_KEY,
                MAILGUN_DOMAIN_NAME,
                DEFAULT_EMAIL_DESTINATION,
            )
        )
        assert all(
            (
                isinstance(value, str)
                for value in (
                    EMAIL_HOST_USER,
                    MAILGUN_API_KEY,
                    MAILGUN_DOMAIN_NAME,
                    DEFAULT_EMAIL_DESTINATION,
                )
            )
        )

    def test_form_save(self):
        # Créez un objet request factice avec l'utilisateur connecté
        request = self.factory.get("/")
        request.user = self.user

        # Testez la méthode save du formulaire
        data = {
            "email": DEFAULT_EMAIL_DESTINATION,
        }
        form = PasswordResetForm(data=data)
        assert form.is_valid()
        form.save(request=request)
