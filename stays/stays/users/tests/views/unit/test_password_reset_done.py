import re
from icecream import ic
from django.test import TestCase
from django.urls import reverse

class PasswordResetViewTest(TestCase):
    def test_password_reset_done_view(self):
        # Get the URL for the password reset done view
        password_reset_done_url = reverse('users:password_reset_done')

        # Make a GET request to the password reset done view
        response = self.client.get(password_reset_done_url)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)
        # ic(response.content.decode('utf-8'))
        # # Utilisez une expression régulière pour extraire le titre de la page
        self.assertIn("First Step Done", response.content.decode())
        self.assertIn("Please Check your email address!", response.content.decode())