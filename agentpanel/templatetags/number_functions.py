from django import template

from adminsidecustomer.models import Country, Province

register = template.Library()

@register.simple_tag()
def country_name(id):
    country = Country.objects.values('country_name').filter(pk=id)
    return country[0]['country_name']

@register.simple_tag()
def province_name(id):
    province = Province.objects.values('province_name').filter(pk=id)
    return province[0]['province_name']


