from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  get_user_model
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView 

from users.forms import RegistrationForm, AccountEditionForm, PasswordChangeFromConnectedProfile
from users.models import Profile

# Create your views here.
def create_profile(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)

class CreateUserView(CreateView):
    """Create a new user in the system"""
    form_class = UserCreationForm
    template_name = "stays/signup.html"
    success_url = reverse_lazy("login")


def register(request):
    """Register the user"""
    if request.method == 'POST':
        user = Profile()
        form = RegistrationForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f"Welcome ! Your account is created with your email address {email} !")
            return redirect('login')
    else:        
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})