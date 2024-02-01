import os
import random
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist
from django.template.loader import get_template


def random_error_handler(request, error_code):
    """
    Error handler which supports multiple templates.
    Templates: <error_code>-a.html, <error_code>-b.html, etc.
    """
    templates = [f for f in os.listdir('templates') if f.startswith(f'{error_code}-') and f.endswith('.html')]
    if templates:
        template = random.choice(templates)
        try:
            t = get_template(template)
            return HttpResponseServerError(t.render(request=request))
        except TemplateDoesNotExist:
            pass
    return HttpResponseServerError()
