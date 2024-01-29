from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.db.models import Count
from django.shortcuts import get_object_or_404
from friendship.models import Follow
from django.contrib import messages
from .models import Profile
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth import views as authentication_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.dates import DateDetailView, DayArchiveView, YearArchiveView, MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from .forms import PasswordResetForm
from friendship.models import Follow


from users.forms import RegistrationForm, AccountLoginForm, AccountEditionForm, PublishContentForm, PasswordChangeFromConnectedProfile
from users.models import Profile, ProfileHasPublication

from core.models import Publication
from core.views import get_continent_from_code, find_cities_light_country_name_with_code, find_cities_light_continent_with_country_code
from locations.utils.helpers import get_continent_from_code
from django_countries import countries

# Custom sugar
from cleantext import clean
from neattext.functions import clean_text
from icecream import ic

# Create your views here.

def retrieve_current_user(profile_email):
    current_user = Profile.objects.get(email=profile_email)
    return current_user


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'delete_account.html'
    success_url = reverse_lazy('core:home')

    def get_object(self, queryset=None):
        return retrieve_current_user(self.request.user)


class CreateProfileView(CreateView):
    """Create a new user in the system"""
    model = Profile
    form_class = RegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        email = form.cleaned_data.get('email')
        messages.success(self.request, f"Welcome ! Your account is being created with your email address {email} !")
        return super().form_valid(form)

    def form_invalid(self, form):
        # ic(form.errors.as_data())
        messages.error(self.request, 'Invalid inputs. Please try again.')
        return self.render_to_response(self.get_context_data(form=form))


class AccountLoginView(authentication_views.LoginView):
    """Login with a registered profile"""
    model = Profile
    form_class = AccountLoginForm
    fields = ["email", "password"]
    template_name = "signin.html"
    redirect_authenticated_user = True
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle
    slug_url_kwarg = 'slug'  # Indiquez le nom du paramètre slug dans votre URL

    def get_success_url(self):
        # Assurez-vous que l'utilisateur est connecté
        if self.request.user.is_authenticated:
            # Essayez de récupérer le profil associé à l'utilisateur
            profile = retrieve_current_user(self.request.user)
            if profile:
                # Récupérez le slug du profil
                user_slug = profile.slug
                return reverse_lazy('users:account', kwargs={'slug': user_slug})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def form_invalid(self, form):
        # ic(form.errors.as_data())
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class AccountDetailsView(DetailView):
    model = Profile
    template_name = "account.html"
    http_method_names = ['get', 'post']
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle
    slug_url_kwarg = 'slug'  # Indiquez le nom du paramètre slug dans votre URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        user_email = context.get("profile")
        context["current_user"] =  retrieve_current_user(user_email)


        context["number_of_publications"] = ProfileHasPublication.objects.filter(user_profile=self.request.user.slug).count()


        context["number_of_followers"] = Follow.objects.filter(followee=self.request.user).count()


        context["number_of_following"] = Follow.objects.filter(follower=self.request.user).count()

        context["current_user"] = self.request.user

        return context



class ProfileStaysListView(ListView):
    model = ProfileHasPublication
    template_name = 'stays.html'

    def get_queryset(self):
        # Récupérer le slug de l'URL
        slug = self.kwargs.get('slug')

        # Récupérer le profil correspondant au slug
        profile = get_object_or_404(Profile, slug=slug)

        # Récupérer toutes les instances de ProfileHasPublication qui correspondent à ce profil
        profile_has_publications = ProfileHasPublication.objects.filter(user_profile=profile)

        # Récupérer les UUIDs des publications
        publication_uuids = profile_has_publications.values_list('publication_of_user__uuid', flat=True)

        # Récupérer toutes les publications qui correspondent à ces UUIDs
        publications = Publication.objects.filter(uuid__in=publication_uuids)
        publications.author_username = profile.username
        publications.author_slug = profile.slug
        publications.author_motto = f'" {profile.motto} "'.upper()

        for publication in publications:
            stay_country_name = find_cities_light_country_name_with_code(publication.country_code_of_stay)
            publication.stay_country_name = stay_country_name

            stay_continent_code = find_cities_light_continent_with_country_code(publication.country_code_of_stay)
            publication.stay_continent_code = get_continent_from_code(stay_continent_code)

            published_from_country_name = find_cities_light_country_name_with_code(publication.published_from_country_code)
            publication.published_from_country_name = published_from_country_name

        return publications

    def get_context_data(self, **kwargs):
        # Obtenir le contexte existant
        context = super().get_context_data(**kwargs)

        # Ajouter les publications au contexte
        context['publications'] = self.get_queryset()

        paginator = Paginator(context['publications'], 100)

        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj

        return context


class UpdateAccountView(UpdateView):
    model = Profile
    form_class = AccountEditionForm
    template_name = "settings.html"
    slug_field = 'slug'  # Indiquez le nom du champ slug dans votre modèle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_email = context.get("profile")
        current_user = retrieve_current_user(user_email)

        UpdateAccountView.success_url = reverse_lazy('users:account', args=[current_user.slug])
        
        context["current_user"] =  current_user
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        about_text = form.cleaned_data.get('about_text')
        if about_text:
            about_text = clean_text(about_text, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=True, multiple_whitespaces=True, special_char=True, emojis=False, stopwords=True)

        signature = form.cleaned_data.get('signature')

        if signature:
            signature = clean_text(signature, urls=True, emails=True, phone_num=True, numbers=True, currency_symbols=True, multiple_whitespaces=True, special_char=True, emojis=False, stopwords=True)

        # Enregistrement de la publication
        profile = form.save(commit=False)
        profile.about_text = about_text
        profile.signature = signature
        profile.save()

        messages.success(self.request, 'Profile updated successfully!')

        return super(UpdateAccountView, self).form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Unsuccessful update due to invalid submitted data. Please check your input.')
        return self.render_to_response(self.get_context_data(form=form))


class PublishView(FormView, CreateView):
    template_name = 'publish.html'  # replace with your actual template
    model = Publication
    form_class = PublishContentForm
    slug_field = 'author_slug'  # Indiquez le nom du champ slug dans votre modèle

    def get_publication_origin(self):
        g = GeoIP2()
        remote_addr = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if remote_addr:
            address = remote_addr.split(',')[-1].strip()
        else:
            address = self.request.META.get('REMOTE_ADDR')

        country_id = g.country_code(address if address != "127.0.0.1" else "88.175.243.206")
        return country_id

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user_email = self.request.user
        current_user = retrieve_current_user(user_email)
        PublishView.slug_url_kwarg = current_user.slug
        PublishView.success_url = reverse_lazy(
            'users:account', args=[current_user.slug]
        )

        context["current_user"] = current_user
        context["active_from_contry_code"] = self.get_publication_origin()
        context["active_from_contry_name"] = dict(countries)[context["active_from_contry_code"]]
        return context

    def form_valid(self, form):
        text_story = form.cleaned_data.get('text_story')
        voice_story = form.cleaned_data.get('voice_story')

        # Assurez-vous qu'au moins l'un des champs est rempli
        if not text_story and not voice_story:
            messages.error(self.request, 'Please provide either a text story or a voice recording.')
            return self.form_invalid(form)

        # Enregistrement de la publication
        publication = form.save(commit=False)
        publication.author_username = self.request.user.username

        # Enregistrement du texte s'il est fourni
        if text_story:
            publication.text_story = clean(  # Clean the texte
                text_story,
                fix_unicode=True,               # fix various unicode errors
                to_ascii=True,                  # transliterate to closest ASCII representation
                lower=False,                     # lowercase text
                no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
                no_urls=True,                  # replace all URLs with a special token
                no_emails=True,                # replace all email addresses with a special token
                no_phone_numbers=True,         # replace all phone numbers with a special token
                no_numbers=False,               # replace all numbers with a special token
                no_digits=False,                # replace all digits with a special token
                no_currency_symbols=False,      # replace all currency symbols with a special token
                no_punct=False,                 # remove punctuations
                replace_with_punct="",          # instead of removing punctuations you may replace them
                replace_with_url="<URL>",
                replace_with_email="<EMAIL>",
                replace_with_phone_number="<PHONE>",
                replace_with_currency_symbol="<$£>",
                lang="en"                       # set to 'de' for German special handling
            )
            
            if self.request.user.signature and self.request.user.signature != "None":
                publication.text_story += f"\n\n{self.request.user.signature}"


        # Enregistrement de l'enregistrement vocal s'il est fourni
        if voice_story:
            # Assurez-vous que le fichier est bien une piste audio
            if not voice_story.name.endswith(('.mp3', '.wav', '.ogg')):
                messages.error(self.request, 'Invalid audio file format.')
                return self.form_invalid(form)

            publication.voice_story = voice_story

        # Sauvegarde finale
        publication.save()

        messages.success(self.request, 'Publication created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Something went wrong. Please check your input.'
        )
        ic(self.request)
        ic(form)
        ic(form.errors.as_data())
        return self.render_to_response(self.get_context_data(form=form))



class PasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # point this to your template
    success_url = reverse_lazy('users:password_reset_complete')

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        try:
            # Get the profile object based on the slug or raise a 404 error
            profile = get_object_or_404(Profile, slug=self.kwargs.get('slug'))

            # Obtient la valeur correspondante pour "EU"
            continent_fullname = get_continent_from_code(profile.continent_of_birth)
            # Modifie la valeur de profile.continent
            profile.continent_of_birth = continent_fullname
            
            profile.number_of_published_stays = ProfileHasPublication.objects.filter(user_profile=profile.slug).count()

            profile.save()

            return profile

        except ObjectDoesNotExist:
            raise Http404("Désolé, ce profil n'existe plus.")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        viewer = Profile.objects.get(slug=self.request.user.slug)

        if Follow.objects.follows(viewer, profile):
            context['viewer_follow_button'] = '<button id="followButton" type="button" class="btn btn-info text-white fw-bold border border-dark">FOLLOWING</button>'
            context['page_viewer_follows_profile'] = True
        else:
            context['viewer_follow_button'] = '<button id="followButton" type="button" class="btn btn-info text-white fw-bold border border-dark">FOLLOW ME</button>'
            context['page_viewer_follows_profile'] = False

        return context



@login_required
def follow_profile(request, slug):
    # Vérifie si la requête est de type POST
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Récupère le corps de la requête et le convertit en JSON
    relation_request = json.loads(request.body)
    ic(relation_request.get('asking'))
    # Récupère le profil demandeur et le profil cible à partir des slugs
    profile_asking = get_object_or_404(Profile, slug=relation_request.get('asking'))
    profile_asking_slug =Profile.objects.get(email=profile_asking).slug
    profile_target = get_object_or_404(Profile, slug=relation_request.get('target'))

    # Vérifie si l'utilisateur demandeur est l'utilisateur actuel
    if profile_asking_slug != request.user.slug:
        ic(f"{profile_asking_slug} != {request.user.slug}")
        return JsonResponse({"error": "Invalid asking user"}, status=400)

    # Vérifie la valeur de "relation"
    ic(relation_request.get('relation'))
    if relation_request.get('relation') == 'follow':



        # Si "relation" est "follow", commence à suivre le profil
        Follow.objects.add_follower(profile_asking, profile_target)
        messages.success(request, f"You are now following {profile_target.username}")
        # Renvoie une réponse HTTP 201 (Created)
        return HttpResponse(status=201)

    elif relation_request.get('relation') == 'unfollow':
        # Si "relation" est "unfollow", arrête de suivre le profil
        Follow.objects.remove_follower(profile_asking, profile_target)
        messages.success(request, f"You have unfollowed {profile_target.username}")
        # Renvoie une réponse HTTP 204 (No Content)
        return HttpResponse(status=204)

    else:
        # Si "relation" n'est ni "follow" ni "unfollow", renvoie une erreur
        return JsonResponse({"error": "Invalid relation value"}, status=400)


class FollowersListView(ListView):
    model = Profile
    template_name = 'followers.html'  # Ajustez ceci à votre template
    context_object_name = 'followers'

    def get_queryset(self):
        profile = get_object_or_404(Profile, slug=self.kwargs['slug'])
        return Follow.objects.followers(profile)


class FollowingListView(ListView):
    model = Follow
    template_name = 'following.html'
    context_object_name = 'stayers'

    def get_queryset(self):
        profile = get_object_or_404(Profile, slug=self.kwargs['slug'])
        queryset = Follow.objects.filter(follower=profile).select_related('followee')
        queryset = queryset.annotate(publication_count=Count('followee__profilehaspublication'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, slug=self.kwargs['slug'])
        context['follower_of_stayer'] = profile.slug
        context['username_of_follower'] = profile.username
        return context




