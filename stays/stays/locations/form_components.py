from django_select2 import forms as s2forms
from .models import Location

class BaseAutocompleteSelect(s2forms.ModelSelect2Widget):
    class Media:
        js = ("admin/js/vendor/jquery/jquery.min.js",)

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.attrs = {"style": "width: 300px"}

    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs = super().build_attrs(base_attrs, extra_attrs)
        base_attrs.update(
            {"data-minimum-input-length": 0, "data-placeholder": self.empty_label}
        )
        return base_attrs
    
class CountryAutocompleteWidget(BaseAutocompleteSelect):
    empty_label = "-- select country --"
    search_fields = ("name__icontains",)
    queryset = Location.objects.filter(
        type="Romance"
    ).order_by("id")