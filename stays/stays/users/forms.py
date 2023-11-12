from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm

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
    profile_picture=forms.ImageField(required=False)
    username=forms.CharField(required=False)
    first_name=forms.CharField(required=False)
    last_name=forms.CharField(required=False)
    season_of_birth=forms.CharField(required=False)
    year_of_birth=forms.IntegerField(required=False)
    about_text=forms.Textarea()
    motto=forms.CharField(required=False)
    signature=forms.CharField(required=False)

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

class PasswordChangeFromConnectedProfile(PasswordChangeForm):
    class Meta:
        model = Profile
        fields = [
            "password"
        ]

