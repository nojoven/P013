from cities_light.models import CONTINENT_CHOICES
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import \
    PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from core.models import Publication
from stays.settings import (DEFAULT_EMAIL_DESTINATION, EMAIL_HOST_USER,
                            MAILGUN_API_KEY, MAILGUN_DOMAIN_NAME)
from stays.utils.email_helpers import send_password_reset_email
from users.models import Profile
from users.utils import (forge_token, generate_recovery_url,
                         generate_reset_uid, get_email_to_user)


class RegistrationForm(UserCreationForm):
    email = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ["username", "email", "password1", "password2"]


# Dans votre formulaire
class UserNotFoundError(Exception):
    pass


class PasswordResetForm(DjangoPasswordResetForm):
    def save(self, request=None, **kwargs):
        # Ensure use_https is not in kwargs
        kwargs.pop("use_https", None)
        # Ensure email_template_name is not in kwargs
        kwargs.pop("email_template_name", None)

        # Get the user who requested the password reset
        self.email_to = self.cleaned_data.get(
            "email", DEFAULT_EMAIL_DESTINATION
        )  # if not DEFAULT_EMAIL_DESTINATION else DEFAULT_EMAIL_DESTINATION

        self.user = get_email_to_user(self)

        # Generate the password reset token
        self.token = forge_token(self.user)

        # Generate the uid
        self.uid = generate_reset_uid(self.user.pk)

        # Build the password reset link
        self.recovery_url = generate_recovery_url(request, self.uid, self.token)

        send_password_reset_email(
            recovery_url=self.recovery_url,
            destination_email=self.email_to,
            domain_name=MAILGUN_DOMAIN_NAME,
            api_key=MAILGUN_API_KEY,
            from_email=EMAIL_HOST_USER,
        )


class AccountLoginForm(AuthenticationForm):
    username = forms.EmailField(required=False)
    password = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ["username", "password"]


class AccountEditionForm(UserChangeForm):
    """Update form for the currennt authenticated profile."""

    profile_picture = forms.ImageField(required=False, allow_empty_file=True)
    username = forms.CharField(required=False, empty_value="Username")
    first_name = forms.CharField(required=False, empty_value="First Name")
    last_name = forms.CharField(required=False, empty_value="Last Name")
    season_of_birth = forms.CharField(required=False, empty_value="Spring")
    year_of_birth = forms.IntegerField(required=False)
    about_text = forms.CharField(required=False, empty_value="Once upon a time...")
    motto = forms.CharField(required=False, empty_value="I LOVE THIS WEBSITE!")
    signature = forms.CharField(required=False, empty_value="Myself!")
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


class PublishCountrySelectWidget(CountrySelectWidget):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Use the custom list of countries from settings
        return context


class PublishContentForm(forms.ModelForm):
    content_type = forms.CharField(required=True)
    title = forms.CharField(required=True)
    author_slug = forms.SlugField(required=True)
    author_username = forms.CharField(required=True)
    country_code_of_stay = CountryField().formfield()
    published_from_country_code = CountryField(default="IT").formfield(required=True)
    summary = forms.CharField(required=True)
    picture = forms.FileField(required=True, allow_empty_file=False)
    year_of_stay = forms.IntegerField(required=True)
    season_of_stay = forms.CharField(required=False, empty_value="Spring")
    text_story = forms.CharField(required=False, empty_value="")
    voice_story = forms.FileField(required=False, allow_empty_file=True)

    class Meta:
        model = Publication
        fields = [
            "title",
            "author_slug",
            "author_username",
            "author_username",
            "country_code_of_stay",
            "published_from_country_code",
            "year_of_stay",
            "season_of_stay",
            "summary",
            "picture",
            "content_type",
            "text_story",
            "voice_story",
        ]
        widgets = {"country_code_of_stay": PublishCountrySelectWidget()}


class PasswordChangeFromConnectedProfile(PasswordChangeForm):
    class Meta:
        model = Profile
        fields = ["password"]
