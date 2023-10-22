from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

from .models import Profile

class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = [ 
            'email',
            'password1',
            'password2'
        ]

class AccountEditionForm(UserChangeForm):
    # Hide the password field
    password = None
    class Meta:
        model = Profile
        fields = [
            'username',
        ]

class PasswordChangeFromConnectedProfile(PasswordChangeForm):
    class Meta:
        model = Profile
        fields = [
            'password'
        ]

