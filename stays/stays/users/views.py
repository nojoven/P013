import time

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as authentication_views
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic.base import TemplateView
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
    # fields = ["email", "password1", "password2"]

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        email = form.cleaned_data.get('email')
        messages.success(self.request, f"Welcome ! Your account is being created with your email address {email} !")
        return super().form_valid(form)


# def register(request):
#     """Register the user"""
#     if request.method == 'POST':
#         user = Profile()
#         form = RegistrationForm(request.POST or None, instance=user)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             messages.info(request, f"Welcome ! Your account is created with your email address {email} !")
#             time.sleep(2)
#             return redirect('login')
#     else:
#         form = RegistrationForm()
#     return render(request, 'signup.html', {'form': form})

# @login_required
def myaccount(request, **kwargs):
    return render(request,"account.html")


class AccountLoginView(authentication_views.LoginView):
    model = Profile
    form_class = AccountLoginForm
    fields = ["email", "password"]
    template_name = "signin.html"
    redirect_authenticated_user = True
    # success_url = reverse_lazy("myaccount")

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






