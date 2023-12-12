from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Publication
from iommi import Form, Field, Action



# PublishForm = Form.create(auto__model=Publication)