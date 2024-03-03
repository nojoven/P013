from django import forms
from core.models import Publication
from core.utils.models_helpers import ContentTypes
from icecream import ic

# class UpdateStayCountrySelectWidget(CountrySelectWidget):
#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, value, attrs)
#         # Use the custom list of countries from settings
#         # context['widget']['optgroups'] = self.optgroups(name, settings.COUNTRIES_LIST, context['widget']['value'])
#         return context

class PublicationEditForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'season_of_stay', 'year_of_stay', 'summary', 'text_story', 'voice_story', 'content_type', 'country_code_of_stay', 'published_from_country_code', 'picture', 'upvotes_count']
        widgets = {
            'voice_story': forms.FileInput(attrs={'no_clear': True}),
            'picture': forms.FileInput(attrs={'no_clear': True})
        
        }

    def __init__(self, *args, **kwargs):
        super(PublicationEditForm, self).__init__(*args, **kwargs)
        ic(self.fields)
        ic(self.instance)
        if self.instance.content_type == ContentTypes.voice.value[0]:
            self.fields['text_story'].disabled = True
            self.fields['voice_story'].required = True
        elif self.instance.content_type == ContentTypes.text.value[0]:
            self.fields['voice_story'].disabled = True
            self.fields['text_story'].required = True
        
        self.fields['title'].required = False
        self.fields['year_of_stay'].required = False
        self.fields['season_of_stay'].required = False
        self.fields['summary'].required = False
        self.fields['country_code_of_stay'].required = False
        self.fields['published_from_country_code'].required = False
        self.fields['picture'].required = False
        self.fields['upvotes_count'].required = False
        self.fields['content_type'].required = False


class ContactAdminForm(forms.Form):
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
