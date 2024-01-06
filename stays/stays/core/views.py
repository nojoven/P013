import json
import os

from django.shortcuts import render
from django.http import HttpResponse
from users.models import Profile
from core.models import Publication
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from locations.models import StayCountry

from icecream import ic


def get_author_picture_from_slug(author_slug: str):
    author_slug = author_slug
    author_profile = Profile.objects.get(slug=author_slug)
    return author_profile.profile_picture


def get_names_from_country_code(country_code: str):
    stay_country = StayCountry.objects.get(country_code_of_stay=country_code)
    return {"country": stay_country.country_name, "continent": stay_country.continent_name}


def get_continent_from_code(continent_code: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, 'utils', 'continents.json')

    with open(json_file_path) as json_file:
        mapping = json.load(json_file)
        return mapping.get(continent_code)

# Create your views here.
def home(request):
    profiles = Profile.objects.all()
    # profiles = Profile.objects.all().filter(is_superuser=False)
    publications = Publication.objects.all().order_by('-created_at')
    paginator = Paginator(publications, 3)

    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'profiles_list': profiles,
        'publications_list': publications,
        'page_obj': page_obj
    }
    return render(request, 'feed.html', context)


class PublicationDetailView(DetailView):
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

        stay_country_data = get_names_from_country_code(
            publication.country_code_of_stay
        )

        

        context["author_profile_picture"] = author_profile_picture
        context["stay_country_name"] = stay_country_data.get("country")
        context["stay_continent_name"] = get_continent_from_code(stay_country_data.get("continent"))

        ic(context.items())
        return context


# django-cool-pagination CBV example
# https://github.com/joe513/django-cool-pagination#cbv-class-based-view
# class Listing(ListView):
#     model = Item
#     paginate_by = 5