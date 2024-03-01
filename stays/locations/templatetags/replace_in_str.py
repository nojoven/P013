from django import template
from icecream import ic
register = template.Library()


@register.filter
def replace_underscore_with_space(value):
    return value.replace("_", " ")