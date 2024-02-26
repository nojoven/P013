from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # /home
    path("", views.home, name="home"),
    path('publications/publication/<uuid:publication_uuid>/picture', views.serve_publication_picture, name='serve_publication_picture'),
    path('publications/publication/<uuid:publication_uuid>/audio', views.serve_publication_audio, name='serve_publication_audio'),
    path("publications/publication/rm", views.PublicationDeleteView.as_view(), name="delete_publication"),
    path("publications/publication/<uuid:uuid>", views.PublicationDetailView.as_view(), name="publication"),
    path("publications/publication/<uuid:pk>/edit", views.PublicationUpdateView.as_view(), name="edit_publication"),
    path('publications/publication/<uuid:uuid>/upvote', views.toggle_upvote, name='upvote'),
    path('publications/publication/<uuid:uuid>/check_user_upvoted', views.check_user_upvoted_publication, name='check_user_upvoted'),
    path("contact", views.ContactAdminView.as_view(), name="contact"),
]
