from django import template


register = template.Library()

@register.filter
def floatformat_dot(value):
    if type(value) == float:
        return '{:.2f}'.format(round(value, 2))

@register.filter
def multiply(a, b):
    return '{:.2f}'.format(round(a*b, 2))


