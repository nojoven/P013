import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.dates import DateDetailView, DayArchiveView, YearArchiveView, MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator

from users.forms import RegistrationForm, AccountEditionForm, PasswordChangeFromConnectedProfile
from users.models import Profile

# Create your views here.


# class CreateProfileView(CreateView):
#     """Create a new user in the system"""
#     model = Profile
#     form_class = RegistrationForm
#     template_name = "signup.html"
#     success_url = reverse_lazy("login")
#     print("**********A***************************************************************")
    

    #fields = ["email", "password1", "password2"]

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     email = form.cleaned_data.get('email')
    #     messages.success(self.request, f"Welcome ! Your account is being created with your email address {email} !")
    #     time.sleep(120)
    #     return super().form_valid(form)


def register(request):
    """Register the user"""
    print(request.method)
    if request.method == 'POST':
        print(request.method+ " ****B************\n*******************************\n****************************") 
        user = Profile()
        form = RegistrationForm(request.POST or None, instance=user)
        print(form.has_error("email"))
        print(form.has_error("password1"))
        print(form.has_error("password2"))
        print(form.is_valid())
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            # messages.info(request, f"Welcome ! Your account is created with your email address {email} !")
            # time.sleep(15)
            return redirect('login')
    else:        
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})