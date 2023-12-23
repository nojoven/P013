from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm

from core.models import Publication

from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = [ 
            "email",
            "password1",
            "password2"
        ]

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
        ]

    # template_name_suffix = "_update_form"




class PublishContentForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'author_slug', 'author_username', 'author_username', 'location_of_stay', 'year_of_stay', 'summary', 'picture']  # replace with your actual fields



class PasswordChangeFromConnectedProfile(PasswordChangeForm):
    class Meta:
        model = Profile
        fields = [
            "password"
        ]

