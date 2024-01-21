from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as authentication_views
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.utils.encoding import force_bytes
from django.views.generic.dates import DateDetailView, DayArchiveView, YearArchiveView, MonthArchiveView, ArchiveIndexView, TodayArchiveView, WeekArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from .forms import PasswordResetForm
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

from users.forms import RegistrationForm, AccountLoginForm, AccountEditionForm, PublishContentForm, PasswordChangeFromConnectedProfile
from users.models import Profile

from core.models import Publication

from django_countries import countries

# Custom sugar
from cleantext import clean
from neattext.functions import clean_text
from icecream import ic

# Create your views here.

def retrieve_current_user(profile_email):
    current_user = Profile.objects.get(email=profile_email)
    return current_user


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'delete_account.html'
    success_url = reverse_lazy('core:home')

    def get_object(self, queryset=None):
        return retrieve_current_user(self.request.user)


class CreateProfileView(CreateView):
    """Create a new user in the system"""
    model = Profile
    form_class = RegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        email = form.cleaned_data.get('email')
        messages.success(self.request, f"Welcome ! Your account is being created with your email address {email} !")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # ic(form.errors.as_data())
        messages.error(self.request,'Invalid inputs. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))


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
            profile = retrieve_current_user(self.request.user)
            if profile:
                # Récupérez le slug du profil
                user_slug = profile.slug
                return reverse_lazy('users:account', kwargs={'slug': user_slug})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def form_invalid(self, form):
        # ic(form.errors.as_data())
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class AccountDetailsView(DetailView):
    model = Profile
    template_name = "account.html"
    http_method_names = ['get', 'post']
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle
    slug_url_kwarg = 'slug'  # Indiquez le nom du paramètre slug dans votre URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        user_email = context.get("profile")
        context["current_user"] =  retrieve_current_user(user_email)
        return context



class ProfileStaysListView(ListView):
    pass


class UpdateAccountView(UpdateView):
    model = Profile
    form_class = AccountEditionForm
    template_name = "settings.html"
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_email = context.get("profile")
        current_user = retrieve_current_user(user_email)

        UpdateAccountView.success_url = reverse_lazy('users:account', args=[current_user.slug])
        
        context["current_user"] =  current_user
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        about_text = form.cleaned_data.get('about_text')
        if about_text:
            about_text = clean_text(about_text, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=True, emojis=True)

        signature = form.cleaned_data.get('signature')

        if signature:
            signature = clean_text(signature, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=True, emojis=False)

        # Enregistrement de la publication
        profile = form.save(commit=False)
        profile.about_text = about_text
        profile.signature = signature
        profile.save()

        messages.success(self.request, 'Profile updated successfully!')

        return super(UpdateAccountView, self).form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Unsuccessful update due to invalid submitted data. Please check your input.')
        return self.render_to_response(self.get_context_data(form=form))


class PublishView(FormView, CreateView):
    template_name = 'publish.html'  # replace with your actual template
    model = Publication
    form_class = PublishContentForm
    slug_field = 'author_slug'  # Indiquez le nom du champ slug dans votre modèle

    def get_publication_origin(self):
        g = GeoIP2()
        remote_addr = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if remote_addr:
            address = remote_addr.split(',')[-1].strip()
        else:
            address = self.request.META.get('REMOTE_ADDR')

        country_id = g.country_code(address if address != "127.0.0.1" else "88.175.243.206")
        return country_id

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user_email = self.request.user
        current_user = retrieve_current_user(user_email)
        PublishView.slug_url_kwarg = current_user.slug
        PublishView.success_url = reverse_lazy(
            'users:account', args=[current_user.slug]
        )

        context["current_user"] = current_user
        context["active_from_contry_code"] = self.get_publication_origin()
        context["active_from_contry_name"] = dict(countries)[context["active_from_contry_code"]]
        return context

    def form_valid(self, form):
        text_story = form.cleaned_data.get('text_story')
        voice_story = form.cleaned_data.get('voice_story')

        # Assurez-vous qu'au moins l'un des champs est rempli
        if not text_story and not voice_story:
            messages.error(self.request, 'Please provide either a text story or a voice recording.')
            return self.form_invalid(form)

        # Enregistrement de la publication
        publication = form.save(commit=False)
        publication.author_username = self.request.user.username

        # Enregistrement du texte s'il est fourni
        if text_story:
            publication.text_story = clean(  # Clean the texte
                text_story,
                fix_unicode=True,               # fix various unicode errors
                to_ascii=True,                  # transliterate to closest ASCII representation
                lower=False,                     # lowercase text
                no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
                no_urls=True,                  # replace all URLs with a special token
                no_emails=True,                # replace all email addresses with a special token
                no_phone_numbers=True,         # replace all phone numbers with a special token
                no_numbers=False,               # replace all numbers with a special token
                no_digits=False,                # replace all digits with a special token
                no_currency_symbols=False,      # replace all currency symbols with a special token
                no_punct=False,                 # remove punctuations
                replace_with_punct="",          # instead of removing punctuations you may replace them
                replace_with_url="<URL>",
                replace_with_email="<EMAIL>",
                replace_with_phone_number="<PHONE>",
                replace_with_currency_symbol="<$£>",
                lang="en"                       # set to 'de' for German special handling
            )

        # Enregistrement de l'enregistrement vocal s'il est fourni
        if voice_story:
            # Assurez-vous que le fichier est bien une piste audio
            if not voice_story.name.endswith(('.mp3', '.wav', '.ogg')):
                messages.error(self.request, 'Invalid audio file format.')
                return self.form_invalid(form)

            publication.voice_story = voice_story

        # Sauvegarde finale
        publication.save()

        messages.success(self.request, 'Publication created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Something went wrong. Please check your input.'
        )
        ic(self.request)
        ic(form)
        ic(form.errors.as_data())
        return self.render_to_response(self.get_context_data(form=form))



class PasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # point this to your template
    success_url = reverse_lazy('users:password_reset_complete')

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
