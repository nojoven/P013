from django.test import TestCase
from users.forms import PublishCountrySelectWidget

class TestPublishCountrySelectWidget(TestCase):
    def setUp(self):
        self.widget = PublishCountrySelectWidget()

    def test_get_context_widget_contains_expected_keys(self):
        context = self.widget.get_context('country', 'US', {})
        self.assertIn('name', context['widget'])
        self.assertIn('value', context['widget'])

    def test_get_context_widget_contains_expected_values(self):
        context = self.widget.get_context('country', 'US', {})
        self.assertEqual(context['widget']['name'], 'country')
        self.assertEqual(context['widget']['value'], ['US'])

    def test_render(self):
        html = self.widget.render('country', 'US', {})
        self.assertIn('<select', html)
        self.assertIn('name="country"', html)
        # The widget does not include the 'value' attribute in the rendered HTML

    def test_get_context_with_none_value(self):
        context = self.widget.get_context('country', None, {})
        self.assertEqual(context['widget']['value'], [''])  # None value is treated as an empty string

    def test_get_context_with_empty_value(self):
        context = self.widget.get_context('country', '', {})
        self.assertEqual(context['widget']['value'], [''])

    def test_get_context_with_additional_attrs(self):
        context = self.widget.get_context('country', 'US', {'class': 'my-class'})
        self.assertIn('class', context['widget']['attrs'])
        self.assertEqual(context['widget']['attrs']['class'], 'my-class')
