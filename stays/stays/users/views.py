from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  get_user_model

# Create your views here.
def create_profile(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)

