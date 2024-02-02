from django.urls import path
from . import views
from core.models import Publication
from iommi import Table, Column, EditTable 

app_name = 'core'

urlpatterns = [
    # /home
    path("", views.home, name="home"),
    #path('publications/<slug:slug>/managecontent/', EditTable(auto__model=Publication, columns__edit=Column.edit(), columns__delete=Column.delete()).as_view()),
    # path('publications/<slug:slug>', views.publications_management_table, name='publications_management_table'),
    path("publications/publication/rm", views.PublicationDeleteView.as_view(), name="delete_publication"),
    path("publications/publication/<uuid:uuid>", views.PublicationDetailView.as_view(), name="publication"),
    path("publications/publication/<uuid:pk>/edit", views.PublicationUpdateView.as_view(), name="edit_publication"),
    path('publications/publication/<uuid:uuid>/upvote', views.toggle_upvote, name='upvote'),
    path('publications/publication/<uuid:uuid>/check_user_upvoted', views.check_user_upvoted_publication, name='check_user_upvoted'),
    path("contact", views.ContactAdminView.as_view(), name="contact"),
]
