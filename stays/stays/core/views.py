from django.shortcuts import render
from django.http import HttpResponse
from users.models import Profile
from core.models import Publication

# Create your views here.
def home(request):
    profiles = Profile.objects.all()
    # profiles = Profile.objects.all().filter(is_superuser=False)
    publications = Publication.objects.all().order_by('-created_at')
    context = {
        'profiles_list': profiles,
        'publications_list': publications
    }
    return render(request, 'feed.html', context)