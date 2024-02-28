import json
from django.core.cache import cache
from django.middleware.csrf import get_token
from stays.settings import ADMIN_EMAIL, MAILGUN_API_KEY, MAILGUN_DOMAIN_NAME
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from core.utils.requests_helpers import NeverCacheMixin
from core.forms import PublicationEditForm, ContactAdminForm
from core.models import Publication, PublicationUpvote
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from cities_light.models import Country
from locations.utils.helpers import get_continent_from_code, find_cities_light_country_name_with_code, find_cities_light_continent_with_country_code
from core.utils.models_helpers import get_author_picture_from_slug, get_profile_from_email
from stays.utils.email_helpers import send_contact_form_email
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page, add_never_cache_headers, never_cache

from django.views.decorators.vary import vary_on_cookie
from core.utils.models_helpers import get_publications_for_feed
from icecream import ic
from django.shortcuts import redirect
from django.test.utils import override_settings
from django.http import FileResponse


@never_cache
def serve_publication_picture(request, publication_uuid):
    publication = get_object_or_404(Publication, uuid=publication_uuid)
    return FileResponse(open(publication.picture.path, 'rb'))


@never_cache
def serve_publication_audio(request, publication_uuid):
    publication = get_object_or_404(Publication, uuid=publication_uuid)
    return FileResponse(open(publication.voice_story.path, 'rb'))


@csrf_exempt
@require_GET
@login_required
def check_user_upvoted_publication(request, uuid):
    # Get the slug of the user from the request
    viewer = request.user.slug

    # Check if a PublicationUpvote object exists with the given publication UUID and user slug
    has_upvoted = PublicationUpvote.objects.filter(publication__uuid=uuid, upvote_profile=viewer).exists()

    # Return a JSON response
    return JsonResponse({'has_upvoted': has_upvoted})


@csrf_exempt
@require_POST
@login_required
def toggle_upvote(request, uuid):
    publication_id = uuid
    profile_email = request.POST.get('profile_email', request.user.email)

    publication = Publication.objects.get(uuid=publication_id)
    profile = get_profile_from_email(profile_email)
    
    upvote, created = PublicationUpvote.objects.get_or_create(publication=publication, upvote_profile=profile.slug)
    
    # Get the CSRF token for the current session
    csrf_token = get_token(request)
    
    if created:
        upvote.upvote_value = 1
        publication.upvotes_count = F('upvotes_count') + 1
        upvote.save()
        button_html = f'''
        <button id="upvbtn" 
            type="button" 
            class="btn btn-light btn-outline-info"
            hx-post="/publications/publication/{publication.uuid}/upvote" 
            hx-params='{{"publication_id": "{publication.uuid}", "profile_email": "{request.user.email}", "csrfmiddlewaretoken": "{csrf_token}"}}'
            hx-target="#upvbtn" 
            hx-swap="outerHTML"
            hx-headers='{{"Content-Type":"application/json"}}'>
            <i id="upvotei" class="fa-solid fa-heart fa-heart-circle-check fa-beat-fade fa-sm" style="color: #e22222;" data-fa-i2svg>You Like It</i>
        </button>
        '''
    else:
        publication.upvotes_count = F('upvotes_count') - 1
        publication.save()
        upvote.delete()
        button_html = f'''
        <button id="upvbtn" 
                type="button" 
                class="btn btn-light btn-outline-info"
                hx-post="/publications/publication/{publication.uuid}/upvote" 
                hx-params='{{"publication_id": "{publication.uuid}", "profile_email": "{request.user.email}", "csrfmiddlewaretoken": "{csrf_token}"}}'
                hx-target="#upvbtn" 
                hx-swap="outerHTML"
                hx-headers='{{"Content-Type":"application/json"}}'>
                <i id="upvotei" class="fa-regular fa-heart upvote" style="color: #e22222;" data-fa-i2svg>Upvote</i>
        </button>
        '''
    return HttpResponse(button_html)


# @override_settings(CACHE_MIDDLEWARE_SECONDS=0)
@vary_on_cookie
@cache_page(60 * 6, key_prefix='home_page_{}'.format(Publication.objects.count()))
def home(request):
    page = request.GET.get('page')
    if not page:
        return redirect('{}?page=1'.format(request.path))
    
    publications = get_publications_for_feed(Publication, Country, find_cities_light_country_name_with_code)
    ic(publications)
    paginator = Paginator(publications, 5)
    page_obj = paginator.get_page(page)
    ic(page_obj)
    context = {
        'page_obj': page_obj
    }

    response = render(request, 'feed.html', context)

    # Check if the user has recently modified the Publication table
    if request.session.get('force_renew_session', False):
        add_never_cache_headers(response)
        # Reset the session variable
        request.session['force_renew_session'] = False

    return response

class PublicationDeleteView(NeverCacheMixin,LoginRequiredMixin, DeleteView):
    model = Publication
    success_url = reverse_lazy('core:home')

    # @never_cache
    # @method_decorator(csrf_exempt)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        identifier = body.get('identifier')

        if identifier:
            Publication.objects.filter(uuid=identifier).delete()
            return JsonResponse({'status': 'success'})
        else:
            messages.error(self.request, 'Something went wrong. Please retry later.')
            return JsonResponse({'status': 'error', 'error': 'No identifier provided'})


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # Set the session variable
        self.request.session['force_renew_session'] = True
        self.request.session.save()
        return HttpResponseRedirect(self.get_success_url())


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationEditForm
    template_name = 'update_publication.html'
    exclude_fields = ['upvotes_count', 'content_type', 'published_from_country_code']
    years = list(range(1950, 2025))
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    file_fields = ['picture', 'voice_story']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication_uuid = context['object'].uuid
        publication = cache.get(f'publication_{publication_uuid}')
        if publication is None:
            publication = context['object']
            cache.set(f'publication_{publication_uuid}', publication)
        context["published_from_country_code"] = publication.published_from_country_code
        context['object'] = publication
        context['title'] = context['object'].title
        context['years'] = PublicationUpdateView.years
        context['seasons'] = PublicationUpdateView.seasons
        context['exclude_fields'] = PublicationUpdateView.exclude_fields
        if context['object'].content_type == 'voice':
            context["exclude_fields"].append('text_story')
        elif context['object'].content_type == 'text':
            context["exclude_fields"].append('voice_story')
        return context

    @never_cache
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        # Set the session variable
        self.request.session['force_renew_session'] = True
        self.request.session.save()
        return reverse_lazy('core:publication', args=[str(self.object.uuid)])
    
    def form_valid(self, form):
        messages.success(self.request, 'Publication updated successfully!', extra_tags='base_success')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f'Something went wrong. Please check your input ({", ".join([f.capitalize().replace("_"," ") for f in form.errors.as_data().keys()])}).'
        )
        return super().form_invalid(form)


class PublicationDetailView(LoginRequiredMixin, NeverCacheMixin, DetailView):
    template_name = 'publication.html'  # Replace with your template name
    context_object_name = 'publication'

    def get_object(self):
        publication = get_object_or_404(Publication, uuid=self.kwargs['uuid'])

        author_profile_picture = get_author_picture_from_slug(publication.author_slug)
        publication.author_profile_picture = author_profile_picture

        stay_country_name = find_cities_light_country_name_with_code(publication.country_code_of_stay)
        publication.stay_country_name = stay_country_name

        stay_continent_code = find_cities_light_continent_with_country_code(publication.country_code_of_stay)
        publication.stay_continent_code = get_continent_from_code(stay_continent_code)

        published_from_country_name = find_cities_light_country_name_with_code(publication.published_from_country_code)
        publication.published_from_country_name = published_from_country_name

        self.object = publication

        return publication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        publication = context.get('publication')

        # Check if the current user has upvoted the current publication
        if self.request.user.is_authenticated:
            has_upvoted = PublicationUpvote.objects.filter(publication=publication.uuid, upvote_profile=self.request.user.slug).exists()
        else:
            has_upvoted = False

        context["has_upvoted"] = has_upvoted

        # Get the number of upvotes for the current publication
        total_upvotes_count = PublicationUpvote.objects.filter(publication=publication.uuid).count()

        publication.total_upvotes_count = total_upvotes_count

        return context


class ContactAdminView(FormView):
    template_name = 'contact.html'  # Replace with your template name
    form_class = ContactAdminForm
    success_url = reverse_lazy('core:home')  # Replace with your success url name

    def form_valid(self, form):
        sender_name = form.cleaned_data.get('name', '')
        from_email = form.cleaned_data.get('email', '')
        subject = form.cleaned_data.get('subject', '')
        message = form.cleaned_data.get('message', '')

        if not len(sender_name) or not len(from_email) or not len(message) or not len(subject):
            messages.error(self.request, 'Please fill in all the fields.')
            return super().form_invalid(form)
        else:
            try:
                send_contact_form_email(
                    destination_email=ADMIN_EMAIL,
                    domain_name=MAILGUN_DOMAIN_NAME,
                    api_key=MAILGUN_API_KEY,
                    from_email=from_email,
                    subject=subject,
                    sender_name=sender_name,
                    message=message
                )
                messages.success(self.request, 'Your message has been sent.', extra_tags='base_success')

            except Exception as e:
                messages.error(self.request, 'Something went wrong. Please try again later.')
                return super().form_invalid(form)
        return super().form_valid(form)





if __name__ == '__main__':
    home()
    print(get_continent_from_code('EU'))