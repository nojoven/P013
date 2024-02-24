from core.forms import ContactAdminForm
from django.test import TestCase


class ContactAdminFormTest(TestCase):
    def test_form_with_valid_data(self):
        form = ContactAdminForm({
            'name': 'Test Name',
            'subject': 'Test Subject',
            'email': 'test@example.com',
            'message': 'Test message',
        })
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_email(self):
        form = ContactAdminForm({
            'name': 'Test Name',
            'subject': 'Test Subject',
            'email': 'not a valid email',
            'message': 'Test message',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_form_with_empty_fields(self):
        form = ContactAdminForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['subject'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])
        self.assertEqual(form.errors['message'], ['This field is required.'])