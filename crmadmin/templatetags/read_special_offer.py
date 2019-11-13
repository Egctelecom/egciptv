from django import template

from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice

register = template.Library()

@register.simple_tag()
def get_service_each_category_read(pk):
    servies = ManageServicePrice.objects.values('id', 'service_category_id', 'service_name', 'service_price','service_logo',
                                                'status').filter(service_category_id=pk,special_offer='no')
    return servies

@register.simple_tag()
def get_service_each_category_special_offer(pk):
    servies = ManageServicePrice.objects.values('id', 'service_category_id', 'service_name', 'service_price',
                                                'status').filter(service_category_id=pk,special_offer='yes')
    return servies