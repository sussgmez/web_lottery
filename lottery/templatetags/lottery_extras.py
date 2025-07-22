from django import template
from ..models import Dollar

register = template.Library()

@register.filter
def floatformat_dot(value):
    if type(value) == float:
        return '{:.2f}'.format(round(value, 2))

@register.filter
def multiply(a, b):
    return '{:.2f}'.format(round(a*b, 2))

@register.filter
def get_exchange_rate(created):
    return Dollar.objects.get(pk=1).history.as_of(created).exchange_rate


