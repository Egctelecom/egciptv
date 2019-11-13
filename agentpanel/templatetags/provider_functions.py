from django import template

register = template.Library()

@register.simple_tag()
def multipy(qty,price):
    data = float(price)*float(qty)
    return data