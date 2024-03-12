import os
import random

from django.conf import settings
from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseGone,
                         HttpResponseNotAllowed, HttpResponseNotModified,
                         HttpResponsePermanentRedirect,
                         HttpResponseServerError)
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from icecream import ic

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


def random_error_handler(request, error_code):
    """
    Error handler which supports multiple templates.
    Templates: <error_code>-a.html, <error_code>-b.html, etc.
    """
    ic("random_error_handler")
    ic(request)
    ic(error_code)
    templates_dir = os.path.join(settings.BASE_DIR, "templates")
    templates = [
        f
        for f in os.listdir(templates_dir)
        if f.startswith(f"{error_code}-") and f.endswith(".html")
    ]
    if templates:
        template = random.choice(templates)
    else:
        ic("500-a.html")
        ic(error_code)
        template = "500-a.html"
    try:
        t = get_template(template)

        return HttpResponse(t.render(request=request))
    except TemplateDoesNotExist:
        return HttpResponseServerError("Template does not exist", status=500)


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ic("ErrorHandlerMiddleware")
        ic(request)
        response = self.get_response(request)
        ic(response)
        ic(response.status_code)
        if not 199 < response.status_code <= 300 and response.status_code not in (
            200,
            201,
            204,
            301,
            302,
            304
        ):
            return random_error_handler(request, response.status_code)
        return response

    def process_exception(self, request, exception):
        ic("process_exception")
        ic(request)
        ic(exception)
        try:
            if isinstance(exception, Http404):
                ic("isinstance 404")
                return random_error_handler(request, 404)
            elif isinstance(exception, HttpResponse):
                ic(exception)
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

        except ValueError:
            ic("ValueError")
            response = self.get_response(request)
            ic(response)
            ic(response.status_code)
            return random_error_handler(request, response.status_code)
