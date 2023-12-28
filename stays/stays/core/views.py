from django.shortcuts import render
from django.http import HttpResponse
from users.models import Profile
from core.models import Publication
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from icecream import ic

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
        # published_stay = Publication.objects.get(uuid=publication_id)
        # context["published_stay"] = published_stay
        ic(context.items())
        return context



# django-cool-pagination CBV example
# https://github.com/joe513/django-cool-pagination#cbv-class-based-view
# class Listing(ListView):
#     model = Item
#     paginate_by = 5