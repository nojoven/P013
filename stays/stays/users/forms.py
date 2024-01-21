from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
# from django_select2 import forms as s2forms
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings

from core.models import Publication

from .models import Profile

from cities_light.models import CONTINENT_CHOICES

from stays.settings import DEFAULT_EMAIL_DESTINATION, EMAIL_HOST_USER, EMAIL_HOST, MAILGUN_API_KEY, MAILGUN_DOMAIN_NAME

from icecream import ic
import requests




class RegistrationForm(UserCreationForm):
    email = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]


class PasswordResetForm(DjangoPasswordResetForm):
    def save(self, request=None, **kwargs):
        ic(DEFAULT_EMAIL_DESTINATION)

        # Ensure use_https is not in kwargs
        kwargs.pop('use_https', None)
        # Ensure email_template_name is not in kwargs
        kwargs.pop('email_template_name', None)
        # Call the parent class's save method, but don't send the email yet
        #super().save(request=request, use_https=True, email_template_name='password_reset_email.html', **kwargs)

        # Get the user who requested the password reset
        email = self.cleaned_data.get("email", DEFAULT_EMAIL_DESTINATION) if not DEFAULT_EMAIL_DESTINATION else DEFAULT_EMAIL_DESTINATION
        ic(email)
        user = next(self.get_users(email), None)
        ic(user)

        # Generate the password reset token
        token = default_token_generator.make_token(user)

        # Generate the uid
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build the password reset link
        recovery_url = request.build_absolute_uri(reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

    # Save the token and uid for later
        self.token = token
        self.uid = uid
        self.recovery_url = recovery_url
        self.email = email
        self.user = user

        #email_template_name = 'password_reset_email.html'
        #email_to_send = render_to_string(email_template_name)
        # self.send_password_reset_email(request)
        self.send_simple_message(recovery_url)

    def send_simple_message(self, recovery_url):
        ic("send_simple_message called")
        return requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN_NAME}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Admin User <{EMAIL_HOST_USER}>",
                "to": [self.email],
                "subject": "Password Reset",
                "text": f'Cliquez sur le lien suivant pour réinitialiser votre mot de passe: {recovery_url}'
            }
        )

    # def send_password_reset_email(self, request):
    #     ic("send_password_reset_email called")
    #     # Construct the email
    #     context = {
    #         'email': self.email,
    #         'domain': EMAIL_HOST,  # request.get_host(),
    #         'site_name': 'S T A Y S',
    #         'uid': self.uid,
    #         'user': self.user.username if self.user.username else self.email,
    #         'token': self.token,
    #         'protocol': 'https',  # 'https' if request.is_secure() else 'http',
    #         'url': self.recovery_url
    #     }
    #     email_template_name = 'password_reset_email.html'
    #     email_to_send = render_to_string(email_template_name, context)

    #     # Send the email
    #     send_mail(
    #         'Réinitialisation du mot de passe',
    #         email_to_send,
    #         # 'Cliquez sur le lien suivant pour réinitialiser votre mot de passe: {}'.format(self.url),
    #         EMAIL_HOST_USER,
    #         # None,
    #         [self.email],
    #         fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None
    #     )
    #     ic("TOTO")

class AccountLoginForm(AuthenticationForm):
    username = forms.EmailField(required=False)
    password = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = [ 
            "username",
            "password"
        ]


class AccountEditionForm(UserChangeForm):
    """Update form for the currennt authenticated profile."""
    profile_picture=forms.ImageField(required=False, allow_empty_file=True)
    username=forms.CharField(required=False, empty_value="Username")
    first_name=forms.CharField(required=False, empty_value="First Name")
    last_name=forms.CharField(required=False, empty_value="Last Name")
    season_of_birth=forms.CharField(required=False, empty_value="Spring")
    year_of_birth=forms.IntegerField(required=False)
    about_text=forms.CharField(required=False, empty_value="Once upon a time...")
    motto=forms.CharField(required=False, empty_value="I LOVE THIS WEBSITE!")
    signature=forms.CharField(required=False, empty_value="Myself!")
    continent_of_birth = forms.ChoiceField(choices=CONTINENT_CHOICES, required=False)

    class Meta:
        model = Profile
        exclude = ("date_joined",)
        fields = [
            "profile_picture",
            "username",
            "first_name",
            "last_name",
            "season_of_birth",
            "year_of_birth",
            "about_text",
            "motto",
            "signature",
            "continent_of_birth",
        ]

    # template_name_suffix = "_update_form"





class PublishCountrySelectWidget(CountrySelectWidget):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Use the custom list of countries from settings
        context['widget']['optgroups'] = self.optgroups(name, settings.COUNTRIES_LIST, context['widget']['value'])
        return context


class PublishContentForm(forms.ModelForm):
    content_type = forms.CharField(required=True)
    title = forms.CharField(required=True)
    author_slug = forms.SlugField(required=True)
    author_username = forms.CharField(required=True)
    country_code_of_stay = CountryField().formfield()
    published_from_country_code = CountryField().formfield()
    summary = forms.CharField(required=True)
    picture = forms.FileField(required=True, allow_empty_file=False)
    year_of_stay = forms.IntegerField(required=True)
    season_of_stay = forms.CharField(required=False, empty_value="Spring")
    text_story = forms.CharField(required=False, empty_value="")
    voice_story = forms.FileField(required=False, allow_empty_file=True)

    class Meta:
        model = Publication
        fields = ['title', 'author_slug', 'author_username', 'author_username', 'country_code_of_stay', 'published_from_country_code', 'year_of_stay', 'season_of_stay', 'summary', 'picture', 'content_type', 'text_story', 'voice_story']
        widgets = {"country_code_of_stay": PublishCountrySelectWidget()}


class PasswordChangeFromConnectedProfile(PasswordChangeForm):
    class Meta:
        model = Profile
        fields = [
            "password"
        ]


class DeleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "username"
        ]