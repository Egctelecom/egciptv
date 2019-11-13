from random import randint
from adminsidecustomer.models import Country,Province

from django import template

from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice

register = template.Library()

@register.assignment_tag()
def random_number(length=3):
    return randint(10**(length-1), (10**(length)-1))


#============================================ SERVICE CATEGORY FUNCTIONS ===============================================

@register.simple_tag()
def get_service_category_name(pk):
    servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status').filter(pk=pk)
    servies_category_name = servies_category[0]['service_category_name']
    return servies_category_name

@register.simple_tag()
def get_service_each_category(pk):
    servies = ManageServicePrice.objects.values('id', 'service_category_id', 'service_name', 'service_price',
                                                'status').filter(service_category_id=pk,special_offer='no')
    print(servies)
    return servies
