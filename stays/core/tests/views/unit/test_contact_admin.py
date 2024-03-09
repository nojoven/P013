from django.test import TestCase, Client
from django.urls import reverse
from core.forms import ContactAdminForm


class TestContactAdminView(TestCase):
    def setUp(self):
        # Création d'un client de test
        self.client = Client()
        self.url = reverse("core:contact")

    def test_contact_admin_view_loads(self):
        # Test que la page se charge correctement
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact.html")

    def test_contact_admin_form_displayed(self):
        # Test que le formulaire est affiché
        response = self.client.get(self.url)
        self.assertIsInstance(response.context["form"], ContactAdminForm)

    def test_contact_admin_form_submission_valid(self):
        # Test de la soumission du formulaire avec des données valides
        response = self.client.post(
            self.url,
            {
                "name": "Test User",
                "email": "test@example.com",
                "subject": "Test Subject",
                "message": "Test Message",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirection après la soumission réussie
        self.assertRedirects(
            response, reverse("core:home"), fetch_redirect_response=False
        )

    def test_contact_admin_form_submission_invalid(self):
        # Test de la soumission du formulaire avec des données invalides
        response = self.client.post(
            self.url,
            {
                "name": "",
                "email": "test@example.com",
                "subject": "Test Subject",
                "message": "Test Message",
            },
        )
        self.assertEqual(
            response.status_code, 200
        )  # Pas de redirection après la soumission échouée
        self.assertFormError(response, "form", "name", "This field is required.")
