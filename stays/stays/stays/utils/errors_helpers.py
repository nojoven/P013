from django.http import (
    Http404, HttpResponseForbidden, HttpResponseNotAllowed,
    HttpResponseBadRequest,
    HttpResponseNotModified, HttpResponseGone, HttpResponseServerError,
    HttpResponsePermanentRedirect, HttpResponse
)

# Unauthorized
response_unauthorized = HttpResponse(status=401)

# Temporary Redirect
response_temporary_redirect = HttpResponse(status=307)

# Too Many Requests
response_too_many_requests = HttpResponse(status=429)

# Service Unavailable
response_service_unavailable = HttpResponse(status=503)

# Gateway Timeout
response_gateway_timeout = HttpResponse(status=504)

# Teapot
response_teapot = HttpResponse(status=418)

import os
import random
from http import HTTPStatus
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
import sweetify
from icecream import ic


def random_error_handler(request, error_code):
    """
    Error handler which supports multiple templates.
    Templates: <error_code>-a.html, <error_code>-b.html, etc.
    """
    templates_dir = os.path.join(settings.BASE_DIR, 'templates')
    templates = [f for f in os.listdir(templates_dir) if f.startswith(f'{error_code}-') and f.endswith('.html')]
    ic(templates)
    if templates:
        template = random.choice(templates)
        ic("if")
        ic(template)
    else:
        template = 'other-status.html'
        ic("else")
        ic(template)

    try:
        t = get_template(template)
        ic(t)
        home_url = request.build_absolute_uri(reverse('core:home'))
        ic(home_url)
        status = HTTPStatus(error_code)
        error_message = status.name
        ic(error_message)
        error_description = status.description
        ic(error_description) 
        sweetify.error(request, 'Oops', html='Code: {}, Message: {}, Description: {}. <a href="{}">FEED</a>'.format(error_code, error_message, error_description, home_url), persistent='FEED', icon='error')
        context = {
            'error_code': error_code,
            'error_message': error_message,
            'error_description': error_description,
            'home_url': home_url,
        }
        ic(context)
        return HttpResponse(t.render(request=request, context=context))
    except TemplateDoesNotExist:
        ic(f"Template {template} does not exist")
        return HttpResponseServerError("Template does not exist", status=500)


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not 199 < response.status_code <= 300 and response.status_code not in (200, 201, 204, 301, 302):
            return random_error_handler(request, response.status_code)
        return response

    def process_exception(self, request, exception):
        ic(exception)
        if isinstance(exception, Http404):
            ic(404)
            return random_error_handler(request, 404)
        elif isinstance(exception, HttpResponse):
            if exception.status_code == response_unauthorized.status_code:
                return random_error_handler(request, 401)
            elif exception.status_code == HttpResponseForbidden.status_code:
                return random_error_handler(request, 403)
            elif exception.status_code == HttpResponseNotAllowed.status_code:
                return random_error_handler(request, 405)
            elif exception.status_code == HttpResponseBadRequest.status_code:
                return random_error_handler(request, 400)
            elif exception.status_code == HttpResponseNotModified.status_code:
                return random_error_handler(request, 304)
            elif exception.status_code == HttpResponseGone.status_code:
                return random_error_handler(request, 410)
            elif exception.status_code == response_teapot.status_code:
                return random_error_handler(request, 418)
            elif exception.status_code == HttpResponseServerError.status_code:
                return random_error_handler(request, 500)
            elif exception.status_code == HttpResponsePermanentRedirect.status_code:
                return random_error_handler(request, 301)
            elif exception.status_code == response_temporary_redirect.status_code:
                return random_error_handler(request, 307)
            elif exception.status_code == response_too_many_requests.status_code:
                return random_error_handler(request, 429)
            elif exception.status_code == response_service_unavailable.status_code:
                return random_error_handler(request, 503)
            elif exception.status_code == response_gateway_timeout.status_code:
                return random_error_handler(request, 504)
            else:
                return random_error_handler(request, 500)
