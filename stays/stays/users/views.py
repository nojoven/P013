import time

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as authentication_views
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.dates import DateDetailView, DayArchiveView, YearArchiveView, MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator

from users.forms import RegistrationForm, AccountLoginForm, AccountEditionForm, PasswordChangeFromConnectedProfile
from users.models import Profile

# Create your views here.


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


# @login_required
def myaccount(request, **kwargs):
    current_user = Profile.objects.get(email=request.user)
    context = {"current_user": current_user}
    return render(request,"account.html", context)

# @login_required
def settings(request, **kwargs):
    current_user = Profile.objects.get(email=request.user)
    context = {"current_user": current_user}
    return render(request,"settings.html", context)


class AccountLoginView(authentication_views.LoginView):
    """Login with a registered profile"""
    model = Profile
    form_class = AccountLoginForm
    fields = ["email", "password"]
    template_name = "signin.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('users:myaccount')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def form_invalid(self, form):
        #print(form.errors.as_data())
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class DetailsAccountView(DetailView):
    pass

class UpdateAccountView(UpdateView):
    # slug_url_kwarg = "slug"
    # slug_field = "slug"
    model = Profile
    # fields = [
    #     "profile_picture",
    #     "username",
    #     "first_name",
    #     "last_name",
    #     "year_of_birth",
    #     "season_of_birth",
    #     "motto",
    #     "about_text",
    #     "signature"
    #     ]
    form_class = AccountEditionForm
    template_name = "settings.html"
    success_url = reverse_lazy('users:settings')
    

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def form_invalid(self, form):
        #print(form.errors.as_data())
        messages.error(self.request,'Unsuccessful update due to invalid submitted data. Please check your input.')
        return self.render_to_response(self.get_context_data(form=form))




