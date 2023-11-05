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
            'email',
            'password1',
            'password2'
        ]

class AccountLoginForm(AuthenticationForm):
    username = forms.EmailField(required=False)
    password = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = [ 
            'username',
            'password'
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

