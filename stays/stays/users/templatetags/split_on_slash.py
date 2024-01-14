from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name="split_on_slash")
@stringfilter
def split_on_slash(arg):
    if "/" in arg:
        return arg.split("/")[-1]
    else:
        return arg