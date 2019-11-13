from random import randint
from adminsidecustomer.models import Country,Province,City
from django import template

register = template.Library()



@register.simple_tag()
def get_province_of_country(pk):
    provinces = Province.objects.values('id','country_id','province_name').filter(country_id=pk)
    return provinces



@register.simple_tag()
def get_city_of_province(pk):
    cities = City.objects.values('id','city_name').filter(province_id=pk)
    return cities