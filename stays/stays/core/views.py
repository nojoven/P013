from django.shortcuts import render
from django.http import HttpResponse
from users.models import Profile
from core.models import Publication
from django.core.paginator import Paginator

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

# django-cool-pagination
# https://github.com/joe513/django-cool-pagination#cbv-class-based-view
# class Listing(ListView):
#     model = Item
#     paginate_by = 5