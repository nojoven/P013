import json
import re
from cleantext import clean
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as authentication_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.contrib.gis.geoip2 import GeoIP2
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import (Http404, HttpResponse, HttpResponseNotAllowed,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView
from django_countries import countries
from django_q.tasks import async_task
from friendship.models import Follow
from icecream import ic
from neattext.functions import clean_text

from core.models import Publication
from core.utils.models_helpers import profanity_filter_and_update
from core.utils.requests_helpers import NeverCacheMixin
from locations.utils.helpers import (
    find_cities_light_continent_with_country_code,
    find_cities_light_country_name_with_code, get_continent_from_code)
from users.forms import (AccountEditionForm, AccountLoginForm,
                         PasswordResetForm, PublishContentForm,
                         RegistrationForm)
from users.models import Profile, ProfileHasPublication
from users.utils import retrieve_current_user

# Create your views here.


class DeleteProfileView(NeverCacheMixin, LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "delete_account.html"
    success_url = reverse_lazy("core:home")

    def get_object(self, queryset=None):
        return self.model.objects.get(email=self.request.user.email)

    def delete(self, request, *args, **kwargs):
        messages.success(
            request, "Profile deleted successfully.", extra_tags="base_success"
        )
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object()
        return context

    def handle_no_permission(self):
        messages.error(
            self.request, "You do not have permission to delete this profile."
        )
        return super().handle_no_permission()


class CreateProfileView(NeverCacheMixin, CreateView):
    """Create a new user in the system"""

    model = Profile
    form_class = RegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("users:login")

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(
                reverse_lazy(
                    'users:account',
                    kwargs={
                        "slug": self.request.user.slug
                    }
                )
            )
        

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        email = form.cleaned_data.get("email")
        messages.success(
            self.request,
            f"Welcome ! Your account is being created with your email address {email} !",
            extra_tags="base_success",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f'Something went wrong. Please check your input ({", ".join([f.capitalize().replace("_"," ") for f in form.errors.as_data().keys()])}).',
        )
        return self.render_to_response(self.get_context_data(form=form))


class AccountLoginView(NeverCacheMixin, authentication_views.LoginView):
    """Login with a registered profile"""

    model = Profile
    form_class = AccountLoginForm
    fields = ["email", "password"]
    template_name = "signin.html"
    redirect_authenticated_user = True
    slug_field = "slug"  # field in the model
    slug_url_kwarg = "slug"  # slug in the url (URI parameter)

    def get_success_url(self):
        # Check if the user is connected
        if self.request.user.is_authenticated:
            # Search the user in the database
            profile = retrieve_current_user(self.request.user, self.model)
            if profile:
                # Fetch user's slug
                user_slug = profile.slug
                return reverse_lazy("users:account", kwargs={"slug": user_slug})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # Set the session variable
        cache.clear()
        self.request.session["force_renew_session"] = True
        self.request.session.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        if (
            "fromfeed" in self.request.GET
            and self.request.GET["fromfeed"] == "fromfeed"
        ):
            return JsonResponse({"error": "Invalid username or password"})
        else:
            # Extract the error message
            error_message = form.errors.as_data()[
                list(form.errors.as_data().keys())[0]
            ][0].messages[0]
            # Create the full message
            full_message = f"Validation Error. {error_message}"
            messages.error(
                self.request,
                f'Something went wrong. Please check your input ({", ".join([f.capitalize().replace("_"," ").replace("username","Email") for f in form.errors.as_data().keys()])}).',
            )
            messages.error(self.request, full_message)
            return self.render_to_response(self.get_context_data(form=form))


class AccountDetailsView(NeverCacheMixin, LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "account.html"
    http_method_names = ["get"]
    slug_field = "slug"  # Indiquez le nom du champ slug dans votre modèle
    slug_url_kwarg = "slug"  # Indiquez le nom du paramètre slug dans votre URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the slug from the URL
        slug = self.kwargs.get("slug")

        # Get the profile corresponding to the slug
        current_user = get_object_or_404(self.model, slug=slug)

        context["current_user"] = current_user

        context["number_of_publications"] = ProfileHasPublication.objects.filter(
            user_profile=self.request.user.slug
        ).count()

        context["number_of_followers"] = Follow.objects.filter(
            followee=self.request.user
        ).count()

        context["number_of_following"] = Follow.objects.filter(
            follower=self.request.user
        ).count()

        # Check if the profile has followers
        profile_has_followers = Follow.objects.filter(
            followee=self.request.user
        ).exists()
        context["profile_has_followers"] = profile_has_followers

        # Check if the profile follows other users
        profile_follows_stayers = Follow.objects.filter(
            follower=self.request.user
        ).exists()
        context["profile_follows_stayers"] = profile_follows_stayers

        context["continent_of_birth"] = get_continent_from_code(
            current_user.continent_of_birth
        )
        return context


class ProfileStaysListView(NeverCacheMixin, LoginRequiredMixin, ListView):
    model = ProfileHasPublication
    template_name = "stays.html"

    def get_queryset(self):
        # Récupérer le slug de l'URL
        slug = self.kwargs.get("slug")

        # Récupérer le profil correspondant au slug
        profile = get_object_or_404(Profile, slug=slug)

        # Récupérer toutes les instances de ProfileHasPublication qui correspondent à ce profil
        profile_has_publications = ProfileHasPublication.objects.filter(
            user_profile=profile
        )

        # Récupérer les UUIDs des publications
        publication_uuids = profile_has_publications.values_list(
            "publication_of_user__uuid", flat=True
        )

        # Récupérer toutes les publications qui correspondent à ces UUIDs
        publications = Publication.objects.filter(uuid__in=publication_uuids)
        publications.author_username = profile.username
        publications.author_slug = profile.slug
        publications.author_motto = f'" {profile.motto} "'.upper()

        for publication in publications:
            stay_country_name = find_cities_light_country_name_with_code(
                publication.country_code_of_stay
            )
            publication.stay_country_name = stay_country_name

            stay_continent_code = find_cities_light_continent_with_country_code(
                publication.country_code_of_stay
            )
            publication.stay_continent_code = get_continent_from_code(
                stay_continent_code
            )

            published_from_country_name = find_cities_light_country_name_with_code(
                publication.published_from_country_code
            )
            publication.published_from_country_name = published_from_country_name

        return publications

    def get_context_data(self, **kwargs):
        # Obtenir le contexte existant
        context = super().get_context_data(**kwargs)

        # Ajouter les publications au contexte
        publications = self.get_queryset()

        paginator = Paginator(publications, 9)

        page = self.request.GET.get("page")
        page_obj = paginator.get_page(page)
        context["page_obj"] = page_obj
        context["publications"] = publications

        return context


class UpdateAccountView(NeverCacheMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = AccountEditionForm
    template_name = "settings.html"
    slug_field = "slug"  # Indiquez le nom du champ slug dans votre modèle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_email = context.get("profile")
        current_user = retrieve_current_user(user_email, self.model)

        UpdateAccountView.success_url = reverse_lazy(
            "users:account", args=[current_user.slug]
        )

        context["current_user"] = current_user
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        about_text_input = form.cleaned_data.get("about_text")
        if about_text_input:
            about_text = clean_text(
                about_text_input,
                urls=True,
                emails=True,
                phone_num=True,
                stopwords=False,
            )
            # Split the original and cleaned text into words
            words_input = re.findall(r'\b[\w\'-]+\b', about_text_input)
            words = re.findall(r'\b[\w\'-]+\b', about_text)

            # For each word in the cleaned text, check if an uppercase version of the word exists in the original text
            for i, word in enumerate(words):
                for word_input in words_input:
                    if word.lower() == word_input.lower() and word_input[0].isupper():
                        # If an uppercase version of the word exists, replace the word with the uppercase version
                        words[i] = word_input
                        break

            # Join the words back into a string
            about_text = ' '.join(words)


        signature_input = form.cleaned_data.get("signature")
        if signature_input:
            signature = clean_text(
                signature_input,
                urls=True,
                emails=True,
                phone_num=True,
                stopwords=False,
                special_char=True,
            )

            # Split the original and cleaned text into words
            words_input = re.findall(r'\b[\w\'-]+\b', signature_input)
            words = re.findall(r'\b[\w\'-]+\b', signature)

            # For each word in the cleaned text, check if an uppercase version of the word exists in the original text
            for i, word in enumerate(words):
                for word_input in words_input:
                    if word.lower() == word_input.lower() and word_input[0].isupper():
                        # If an uppercase version of the word exists, replace the word with the uppercase version
                        words[i] = word_input
                        break

            # Join the words back into a string
            signature = ' '.join(words)

        # Enregistrement de la publication
        profile = form.save(commit=False)
        profile.about_text = about_text
        profile.signature = signature
        profile.save()

        messages.success(
            self.request, "Profile updated successfully!", extra_tags="base_success"
        )

        return super(UpdateAccountView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f'Something went wrong. Please check your input ({", ".join([f.capitalize().replace("_"," ") for f in form.errors.as_data().keys()])}).',
        )
        return self.render_to_response(self.get_context_data(form=form))


class PublishView(NeverCacheMixin, LoginRequiredMixin, FormView, CreateView):
    template_name = "publish.html"  # replace with your actual template
    model = Publication
    form_class = PublishContentForm
    slug_field = "author_slug"  # Indiquez le nom du champ slug dans votre modèle

    def get_publication_origin(self):
        g = GeoIP2()
        remote_addr = self.request.META.get("HTTP_X_FORWARDED_FOR")

        if remote_addr:
            address = remote_addr.split(",")[-1].strip()
        else:
            address = self.request.META.get("REMOTE_ADDR")

        country_id = g.country_code(
            address if address != "127.0.0.1" else "88.175.243.206"
        )
        return country_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_email = self.request.user
        current_user = retrieve_current_user(user_email, Profile)
        PublishView.slug_url_kwarg = current_user.slug
        PublishView.success_url = reverse_lazy(
            # 'core:home', args=[current_user.slug]
            "core:home"
        )

        context["current_user"] = current_user
        context["active_from_contry_code"] = self.get_publication_origin()
        context["active_from_contry_name"] = dict(countries)[
            context["active_from_contry_code"]
        ]
        return context

    def form_valid(self, form):
        text_story = form.cleaned_data.get("text_story")
        voice_story = form.cleaned_data.get("voice_story")

        # Assurez-vous qu'au moins l'un des champs est rempli
        if not text_story and not voice_story:
            messages.error(
                self.request, "Please provide either a text story OR a voice recording."
            )
            return self.form_invalid(form)

        # Enregistrement de la publication
        publication = form.save(commit=False)
        publication.author_username = self.request.user.username
        publication.published_from_country_code = self.get_publication_origin()
        publication.updated_at = None

        # Enregistrement de l'enregistrement vocal s'il est fourni
        if voice_story:
            # Assurez-vous que le fichier est bien une piste audio
            if not voice_story.name.endswith((".mp3", ".wav", ".ogg")):
                messages.error(self.request, "Invalid audio file format.")
                return self.form_invalid(form)

            publication.voice_story = voice_story

        # Enregistrement du texte s'il est fourni
        if text_story:
            publication.text_story = clean(  # Clean the texte
                text_story,
                fix_unicode=True,  # fix various unicode errors
                to_ascii=False,  # transliterate to closest ASCII representation
                lower=False,  # lowercase text
                no_line_breaks=False,  # fully strip line breaks as opposed to only normalizing them
                no_urls=True,  # replace all URLs with a special token
                no_emails=True,  # replace all email addresses with a special token
                no_phone_numbers=True,  # replace all phone numbers with a special token
                no_numbers=False,  # replace all numbers with a special token
                no_digits=False,  # replace all digits with a special token
                no_currency_symbols=False,  # replace all currency symbols with a special token
                no_punct=False,  # remove punctuations
                replace_with_punct="",  # instead of removing punctuations you may replace them
                replace_with_url="<URL>",
                replace_with_email="<EMAIL>",
                replace_with_phone_number="<PHONE>",
                replace_with_currency_symbol="<$£>",
                lang="en",  # set to 'de' for German special handling
            )

            if self.request.user.signature and self.request.user.signature != "None":
                publication.text_story += f"\n\n« {self.request.user.signature} »"

        # Sauvegarde finale
        publication.save()

        if publication.text_story:
            # Background task to check for profanity
            async_task(profanity_filter_and_update, publication, timeout=1800)

        messages.success(
            self.request, "Publication created successfully!", extra_tags="base_success"
        )
        # Set the session variable
        self.request.session["force_renew_session"] = True
        self.request.session.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            f'Something went wrong. Please check your input ({", ".join([f.capitalize().replace("_"," ") for f in form.errors.as_data().keys()])}).',
        )
        return self.render_to_response(self.get_context_data(form=form))


class PasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = "password_reset_form.html"
    success_url = reverse_lazy("users:password_reset_done")

    def form_invalid(self, form):
        messages.error(
            self.request, "There was an error in the form. Please check your input."
        )
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                return self.form_valid(form)
            except Exception as e:
                messages.error(request, str(e))
                return self.form_invalid(form)
        return redirect("users:password_reset")


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"  # point this to your template
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"


class ProfileDetailView(NeverCacheMixin, DetailView):
    model = Profile
    template_name = "profile.html"
    context_object_name = "profile"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        try:
            # Get the profile object based on the slug or raise a 404 error
            profile = get_object_or_404(Profile, slug=self.kwargs.get("slug"))

            # Obtient la valeur correspondante pour "EU"
            continent_fullname = get_continent_from_code(profile.continent_of_birth)

            # Modifie la valeur de profile.continent
            profile.continent_of_birth = continent_fullname

            profile.number_of_published_stays = ProfileHasPublication.objects.filter(
                user_profile=profile.slug
            ).count()
            profile.save()
            return profile

        except ObjectDoesNotExist:
            raise Http404("Désolé, ce profil n'existe plus.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        if hasattr(self.request.user, "slug"):
            viewer = Profile.objects.get(slug=self.request.user.slug)

            if Follow.objects.follows(viewer, profile):
                context["viewer_follow_button"] = (
                    '<button id="followButton" type="button" class="btn btn-info text-white fw-bold border border-dark">FOLLOWING</button>'
                )
                context["page_viewer_follows_profile"] = True
            else:
                context["viewer_follow_button"] = (
                    '<button id="followButton" type="button" class="btn btn-info text-white fw-bold border border-dark">FOLLOW ME</button>'
                )
                context["page_viewer_follows_profile"] = False
        return context


@login_required
def follow_profile(request, slug):
    # Vérifie si la requête est de type POST
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    # Récupère le corps de la requête et le convertit en JSON
    relation_request = json.loads(request.body)
    # Récupère le profil demandeur et le profil cible à partir des slugs
    profile_asking = get_object_or_404(Profile, slug=relation_request.get("asking"))
    profile_target = get_object_or_404(Profile, slug=relation_request.get("target"))

    # profile_asking_slug = Profile.objects.get(email=profile_asking).slug
    # # Vérifie si l'utilisateur demandeur est l'utilisateur actuel
    # if profile_asking_slug != request.user.slug:
    #     return JsonResponse({"error": "Invalid asking user"}, status=400)

    # Vérifie la valeur de "relation"
    if relation_request.get("relation") == "follow":
        # Si "relation" est "follow", commence à suivre le profil
        Follow.objects.add_follower(profile_asking, profile_target)

        # Renvoie une réponse HTTP 201 (Created)
        return HttpResponse(status=201)

    elif relation_request.get("relation") == "unfollow":
        # Si "relation" est "unfollow", arrête de suivre le profil
        Follow.objects.remove_follower(profile_asking, profile_target)

        # Renvoie une réponse HTTP 204 (No Content)
        return HttpResponse(status=204)

    else:
        # Si "relation" n'est ni "follow" ni "unfollow", renvoie une erreur
        return JsonResponse({"error": "Invalid relation value"}, status=400)


class FollowersListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "followers.html"  # Ajustez ceci à votre template
    context_object_name = "followers"

    def get_queryset(self):
        profile = get_object_or_404(Profile, slug=self.kwargs["slug"])
        return Follow.objects.followers(profile)


class FollowingListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = "following.html"
    context_object_name = "stayers"

    def get_queryset(self):
        profile = get_object_or_404(Profile, slug=self.kwargs["slug"])
        queryset = Follow.objects.filter(follower=profile).select_related("followee")
        queryset = queryset.annotate(
            publication_count=Count("followee__profilehaspublication")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, slug=self.kwargs["slug"])
        context["follower_of_stayer"] = profile.slug
        context["username_of_follower"] = profile.username
        return context


def logout_view(request):
    # Log out the user
    logout(request)
    # Set the session variable
    request.session["force_renew_session"] = True
    request.session.save()
    # Redirect to a success page.
    cache.clear()
    return HttpResponseRedirect(reverse("core:home"))
