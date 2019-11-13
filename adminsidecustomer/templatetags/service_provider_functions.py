from django import template

from adminsideserviceprovider.models import ServiceProvider,Hardware

register = template.Library()

@register.simple_tag()
def get_service_provider(id):
    data = ServiceProvider.objects.values('id','service_provider_name').filter(pk=id)

    return data[0]['service_provider_name']

@register.simple_tag()
def get_service_provider_hw(id):
    data = Hardware.objects.values('id','hw_title').filter(pk=id)

    return data[0]['hw_title']