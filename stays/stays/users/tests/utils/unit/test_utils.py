from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from model_bakery import baker
from users.forms import PasswordResetForm
from users.utils import get_email_to_user, forge_token, generate_reset_uid, generate_recovery_url
from django.utils import timezone
from stays.settings import DEFAULT_EMAIL_DESTINATION

class TestPasswordResetFormFunctions(TestCase):
    def setUp(self):
        self.user = baker.make('users.Profile', email=DEFAULT_EMAIL_DESTINATION, password='password')
        self.user.last_login = timezone.now()
        self.user.save()

        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

        self.form_data = {
            'email': DEFAULT_EMAIL_DESTINATION,
        }
        self.form = PasswordResetForm(data=self.form_data)
        self.form.email_to = self.form_data['email']

    def test_get_email_to_user(self):
        user = get_email_to_user(self.form)
        self.assertEqual(user, self.user)

    def test_forge_token(self):
        token = forge_token(self.user)
        self.assertTrue(default_token_generator.check_token(self.user, token))

    def test_generate_reset_uid(self):
        uid = generate_reset_uid(self.user.pk)
        self.assertEqual(uid, urlsafe_base64_encode(force_bytes(self.user.pk)))

    def test_generate_recovery_url(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        recovery_url = generate_recovery_url(self.request, uid, token)
        expected_url = self.request.build_absolute_uri(reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(recovery_url, expected_url)