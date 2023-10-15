from django.shortcuts import render
from django.http import HttpResponse
from users.models import Profile
 
# Create your views here.
def home(request):
    profiles = Profile.objects.all().filter(is_superuser=False)
    context = {
        'profiles_list': profiles,
    }
    return render(request, 'index.html', context)