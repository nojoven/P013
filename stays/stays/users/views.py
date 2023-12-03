from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as authentication_views
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.dates import DateDetailView, DayArchiveView, YearArchiveView, MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator

from users.forms import RegistrationForm, AccountLoginForm, AccountEditionForm, PasswordChangeFromConnectedProfile
from users.models import Profile


# Custom sugar
from loguru import logger
from tabulate import tabulate

# Create your views here.

def retrieve_current_user(profile_email):
    current_user = Profile.objects.get(email=profile_email)
    return current_user

class CreateProfileView(CreateView):
    """Create a new user in the system"""
    model = Profile
    form_class = RegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        email = form.cleaned_data.get('email')
        messages.success(self.request, f"Welcome ! Your account is being created with your email address {email} !")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        #print(form.errors.as_data())
        messages.error(self.request,'Invalud inputs. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))


#@login_required
def myaccount(request, **kwargs):
    current_user = Profile.objects.get(email=request.user)
    context = {"current_user": current_user}
    return render(request,"account.html", context)

# @login_required
# def settings(request, **kwargs):
#     current_user = Profile.objects.get(email=request.user)
#     context = {"current_user": current_user}
#     return render(request,"settings.html", context)


class AccountLoginView(authentication_views.LoginView):
    """Login with a registered profile"""
    model = Profile
    form_class = AccountLoginForm
    fields = ["email", "password"]
    template_name = "signin.html"
    redirect_authenticated_user = True
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle
    slug_url_kwarg = 'slug'  # Indiquez le nom du paramètre slug dans votre URL

    def get_success_url(self):
        # Assurez-vous que l'utilisateur est connecté
        if self.request.user.is_authenticated:
            # Essayez de récupérer le profil associé à l'utilisateur
            print(self.request.user)
            profile = retrieve_current_user(self.request.user)
            if profile:
                # Récupérez le slug du profil
                user_slug = profile.slug
                return reverse_lazy('users:myaccount', kwargs={'slug': user_slug})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def form_invalid(self, form):
        #print(form.errors.as_data())
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class AccountDetailsView(DetailView):
    model = Profile
    template_name = "account.html"
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle
    slug_url_kwarg = 'slug'  # Indiquez le nom du paramètre slug dans votre URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        user_email = context.get("profile")
        context["current_user"] =  retrieve_current_user(user_email)
        return context


class UpdateAccountView(UpdateView):
    model = Profile
    form_class = AccountEditionForm
    template_name = "settings.html"
    success_url = reverse_lazy('users:myaccount')
    http_method_names = ['get', 'post']
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle
    slug_url_kwarg = 'slug'  # Indiquez le nom du paramètre slug dans votre URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        user_email = context.get("profile")
        context["current_user"] =  retrieve_current_user(user_email)
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(UpdateAccountView,self).form_valid(form)

    def form_invalid(self, form):
        # print(form.errors.as_data())
        messages.error(self.request,'Unsuccessful update due to invalid submitted data. Please check your input.')
        return self.render_to_response(self.get_context_data(form=form))
    

class UserAction():
    pass





