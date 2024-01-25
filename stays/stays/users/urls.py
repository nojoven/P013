from django.contrib.auth import views as authentication_views
from django.urls import path, include
from users import views



app_name = 'users'

urlpatterns = [
    path("signup", views.CreateProfileView.as_view(), name="signup"),
    path("login", views.AccountLoginView.as_view(template_name='signin.html'), name='login'),
    path("logout", authentication_views.LogoutView.as_view(template_name='signout.html'), name='logout'),
    path('password/reset', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("account/<slug:slug>", views.AccountDetailsView.as_view(), name="account"),
    path("account/<slug:slug>/stays", views.ProfileStaysListView.as_view(), name="stays"),
    path("account/<slug:slug>/publish", views.PublishView.as_view(), name="publish"),
    path("account/<slug:slug>/settings", views.UpdateAccountView.as_view(), name="settings"),
    path("account/<slug:slug>/delete", views.DeleteProfileView.as_view(), name="delete_account"),
    path("", include('allauth.urls')),
    path('profile/<slug:slug>/public', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/<slug:slug>/followtoggle', views.follow_profile, name='follow_unfollow'),
    path('profile/<slug:slug>/following', views.FollowingListView.as_view(), name='following'),

]
