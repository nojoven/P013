import json
from django.middleware.csrf import get_token
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.db.models import F
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from core.utils.requests_helpers import NeverCacheMixin
from core.forms import PublicationEditForm

from core.models import Publication, PublicationUpvote
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from cities_light.models import Country
from locations.utils.helpers import get_continent_from_code, find_cities_light_country_name_with_code, find_cities_light_continent_with_country_code
from icecream import ic
from core.utils.models_helpers import get_author_picture_from_slug, get_profile_from_email, get_all_profiles

from iommi import Table, Column, Action, Form, Field
from iommi import Style, register_style, Asset
from iommi.asset import Asset
from iommi.style import (
    Style,
)
from iommi.style_base import (
    base,
    select2_enhanced_forms,
)
from iommi.style_bootstrap_icons import bootstrap_icons

bootstrap5_base = Style(
    base,
    sub_styles__horizontal=dict(
        Field=dict(
            shortcuts=dict(
                boolean__label__attrs__class={
                    'col-form-label': True,
                },
            ),
            attrs__class={
                'mb-3': False,
                'col-sm-3': True,
                'my-1': True,
            },
        ),
        Form__attrs__class={
            'align-items-center': True,
        },
    ),
    root__assets=dict(
        css=Asset.css(
            attrs=dict(
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
                integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3",
                crossorigin="anonymous",
            ),
        ),
        popper_js=Asset.js(
            attrs=dict(
                src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js",
                integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB",
                crossorigin="anonymous",
            )
        ),
        js=Asset.js(
            attrs=dict(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js",
                integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13",
                crossorigin="anonymous",
            )
        ),
    ),
    Container=dict(
        tag='div',
        attrs__class={
            'container': True,
            'mt-5': True,
            'pt-5': True,
        },
    ),
    Field=dict(
        shortcuts=dict(
            boolean=dict(
                input__attrs__class={'form-check-input': True, 'form-control': False},
                attrs__class={'form-check': True},
                label__attrs__class={'form-label': True},
            ),
            radio=dict(
                attrs__class={
                    'mb-3': False,
                    'form-check': True,
                },
                input__attrs__class={
                    'form-check-input': True,
                    'form-control': False,
                },
            ),
            choice__input__attrs__class={'form-select': True},
        ),
        attrs__class={
            'mb-3': True,
        },
        input__attrs__class={
            'form-control': True,
            'is-invalid': lambda field, **_: bool(field.errors),
        },
        help__attrs__class={
            'form-text': True,
            'text-muted': True,
        },
        label__attrs__class={'form-label': True},
        label__attrs__class__form_label=True,  # need this to make class render
    ),
    FieldGroup=dict(
        tag='div',
        attrs__class={'row': True},
    ),
    Action=dict(
        shortcuts=dict(
            # In bootstrap one must choose a button style (secondary, success, ...)
            # otherwise the styling is roughly identical to text.
            button__attrs__class={
                'btn': True,
                'btn-secondary': True,
            },
            primary__attrs__class={
                'btn-primary': True,
                'btn-secondary': False,
            },
            delete__attrs__class={
                'btn-danger': True,
                'btn-secondary': False,
            },
        ),
    ),
    Table=dict(
        attrs__class__table=True,
        attrs__class={'table-sm': True},
    ),
    Column=dict(
        header__attrs__class={'text-nowrap': True},
        shortcuts=dict(
            select=dict(
                header__attrs__title='Select all',
                header__attrs__class={'text-center': True},
                cell__attrs__class={'text-center': True},
            ),
            number=dict(
                cell__attrs__class={'text-right': True},
                header__attrs__class={'text-right': True},
            ),
            boolean__cell__attrs__class={'text-center': True},
            delete=dict(
                cell__link__attrs__class={'text-danger': True},
            ),
        ),
    ),
    Query=dict(
        form__iommi_style='horizontal',
        form_container=dict(
            tag='span',
            attrs__class={
                'row': True,
                'align-items-center': True,
            },
        ),
    ),
    Menu=dict(
        tag='nav',
        attrs__class={
            'navbar': True,
            'navbar-expand-lg': True,
            'navbar-dark': True,
            'bg-primary': True,
        },
        items_container__attrs__class={'navbar-nav': True},
        items_container__tag='ul',
    ),
    MenuItem=dict(
        tag='li',
        a__attrs__class={'nav-link': True},
        attrs__class={'nav-item': True},
    ),
    Paginator=dict(
        template='iommi/table/bootstrap/paginator.html',
        container__attrs__class__pagination=True,
        active_item__attrs__class={'page-item': True, 'active': True},
        link__attrs__class={'page-link': True},
        item__attrs__class={'page-item': True},
    ),
    Errors=dict(
        attrs__class={'text-danger': True},
    ),
    DebugMenu=dict(
        attrs__class={
            'bg-primary': False,
            'navbar': False,
            'navbar-dark': False,
        },
        items_container__attrs__class={
            'pl-0': True,
            'mb-0': True,
            'small': True,
        },
    ),
    Admin=dict(
        parts__menu=dict(
            # tag='foo',   # TODO: This styling is ignored. We should be able to do this.
            attrs__class={
                'fixed-top': True,
            },
        ),
    ),
    Errors__attrs__class={'with-errors': True},
)
bootstrap5 = Style(
    bootstrap5_base,
    bootstrap_icons,
    select2_enhanced_forms,
)

my_style = bootstrap5

# register_style('my_style', my_style)


# @login_required
# def publications_management_table(request, slug):
#     class PublicationsOfAuthorTable(Table):
#         class Meta:
#             model = Publication
#             rows = Publication.objects.filter(author_slug=slug)
#             columns__edit = Column.edit()
#             columns__delete = Column.delete()

#     table = PublicationsOfAuthorTable().bind(request=request)
#     return HttpResponse(table.__html__())

# @login_required
# def publications_management_table(request, slug):
#     class PublicationsOfAuthorTable(Table):
#         class Meta:
#             model = Publication
#             rows = Publication.objects.filter(slug=slug)
#             style = MyStyle()

#         select = Column.select()
#         title = Column.editable()
#         picture = Column.file()
#         actions = Column.actions(
#             delete=Action.post(
#                 attrs__href=lambda row, **_: f'/delete_publication/{row.pk}/',
#                 include=lambda row, **_: row.author_username == request.user.username
#             )
#         )

#     return PublicationsOfAuthorTable().bind(request=request).render()



@csrf_exempt
@require_GET
def check_user_upvoted_publication(request, uuid):
    # Get the slug of the user from the request
    viewer = request.user.slug

    # Check if a PublicationUpvote object exists with the given publication UUID and user slug
    has_upvoted = PublicationUpvote.objects.filter(publication__uuid=uuid, upvote_profile=viewer).exists()

    # Return a JSON response
    return JsonResponse({'has_upvoted': has_upvoted})


@csrf_exempt
@require_POST
def toggle_upvote(request, uuid):
    publication_id = uuid
    req = request.POST
    ic(req)
    profile_email = None
    for key in req.keys():
        if 'profile_email' in key:
            profile_email = key.split(":")[1].strip(' "')
            ic(profile_email)
            break
        else:
            continue
    ic(profile_email)
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


# Create your views here.
def home(request):
    profiles = get_all_profiles()
    # profiles = Profile.objects.all().filter(is_superuser=False)
    publications = Publication.objects.all().order_by('-created_at')
    for publication in publications:
        # ic(str(publication.country_code_of_stay))
        country_data = Country.objects.get(code2=str(publication.country_code_of_stay))

        publication.stay_country_name = country_data.name
        publication.stay_continent_name = country_data.continent
        if publication.published_from_country_code:
            publication.published_from_country_name = find_cities_light_country_name_with_code(publication.published_from_country_code)
        else:
            publication.published_from_country_name = "" if not publication.published_from_country_code else Country.objects.get(code2=str(publication.country_code_of_stay)).name
    
        publication.upvoters = PublicationUpvote.objects.filter(publication_id=publication.uuid).values_list('upvote_profile', flat=True)

    paginator = Paginator(publications, 3)

    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'profiles_list': profiles,
        'publications_list': publications,
        'page_obj': page_obj
    }
    return render(request, 'feed.html', context)


class PublicationDetailView(NeverCacheMixin, DetailView):
    model = Publication
    template_name = "publication.html"
    slug_field = 'uuid'  # Indiquez le nom du champ slug dans votre modèle
    pk_url_kwarg = 'uuid'  # Indiquez le nom du paramètre slug dans votre URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = context.get("publication")

        author_profile_picture = get_author_picture_from_slug(
            publication.author_slug
        )
        publication.author_profile_picture = author_profile_picture

        stay_country_name = find_cities_light_country_name_with_code(publication.country_code_of_stay)
        publication.stay_country_name = stay_country_name

        stay_continent_code = find_cities_light_continent_with_country_code(publication.country_code_of_stay)
        publication.stay_continent_code = get_continent_from_code(stay_continent_code)

        published_from_country_name = find_cities_light_country_name_with_code(publication.published_from_country_code)
        publication.published_from_country_name = published_from_country_name

        context["publication"] = publication

        # Check if the current user has upvoted the current publication
        if self.request.user.is_authenticated:
            has_upvoted = PublicationUpvote.objects.filter(publication=publication.uuid, upvote_profile=self.request.user.slug).exists()
        else:
            has_upvoted = False

        context["has_upvoted"] = has_upvoted

        ic(context.items())

        return context


class PublicationDeleteView(DeleteView):
    model = Publication
    success_url = reverse_lazy('core:home')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        identifier = body.get('identifier')

        if identifier:
            Publication.objects.filter(uuid=identifier).delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'error': 'No identifier provided'})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class PublicationUpdateView(UpdateView):
    model = Publication
    form_class = PublicationEditForm
    template_name = 'update_publication.html'
    exclude_fields = ['upvotes_count', 'reveal_city', 'content_type', 'published_from_country_code']
    years = list(range(1950, 2025))
    seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
    file_fields = ['picture', 'voice_story']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['years'] = PublicationUpdateView.years
        context['seasons'] = PublicationUpdateView.seasons
        context['exclude_fields'] = PublicationUpdateView.exclude_fields
        if context['object'].content_type == 'voice':
            context["exclude_fields"].append('text_story')
        elif context['object'].content_type == 'text':
            context["exclude_fields"].append('voice_story')
        return context

    def get_success_url(self):
        return reverse_lazy('core:publication', args=[str(self.object.uuid)])
    
    def form_valid(self, form):
        messages.success(self.request, 'Publication updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        ic(form.errors.as_data()) 
        messages.error(self.request, 'Something went wrong. Please check your input.')
        return super().form_invalid(form)


