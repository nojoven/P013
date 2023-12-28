from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # /home
    path("", views.home, name="home"),
    # path("publications", views.PublicationsListView.as_view(), name="account"),
    path("publications/publication/<uuid:uuid>", views.PublicationDetailView.as_view(), name="publication"),
]
