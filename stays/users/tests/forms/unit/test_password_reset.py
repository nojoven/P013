from model_bakery import baker
from django.test import TestCase
from users.forms import PasswordResetForm


class TestPasswordResetForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Créez des instances de modèles nécessaires pour les tests ici
        cls.user = baker.make(
            "users.Profile",
            email="testuser@example.com",
            password="pbkdf2_sha256$216000$B3zYPj1h1FVk$2tLvHHLQ+3m3DzhuwVn2HqWKTV58U6vfEPiUM/U+RQI=",
        )

    def test_form_save(self):
        # Testez la méthode save du formulaire
        data = {
            "email": "testuser@example.com",
        }
        form = PasswordResetForm(data=data)
        assert form.is_valid()
