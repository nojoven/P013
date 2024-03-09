from django.test import TestCase

from users.forms import RegistrationForm


class TestRegistrationForm(TestCase):
    def test_form_save(self):
        # Testez la méthode save du formulaire
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        form = RegistrationForm(data=data)
        if form.is_valid():
            profile = form.save()
            # Vérifiez que le profil a été créé correctement
            self.assertEqual(profile.username, "testuser")
            self.assertEqual(profile.email, "testuser@example.com")
            self.assertTrue(profile.check_password("testpassword123"))
