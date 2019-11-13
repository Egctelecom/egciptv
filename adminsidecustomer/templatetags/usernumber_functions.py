from django import template

from adminnumberprovider.models import NumberProvinceCustomerMap
from adminsidecustomer.models import AccountAddressCustomer

register = template.Library()

@register.simple_tag()
def get_phone_number(id):
    if NumberProvinceCustomerMap.objects.filter(user_id=id).exists():
        data = NumberProvinceCustomerMap.objects.values('id','number_id','number_id__number').filter(user_id=id).order_by('-id')[:1] ##last item of table
        kl = data[0]['number_id__number']
        return kl
    else:
        return 'No number added'


@register.simple_tag()
def get_customer_address(id):

    data = AccountAddressCustomer.objects.values('id','address_1','address_2','city_id__city_name','province_id__province_name','country_id__country_name', 'postal').filter(user_id=id)
    return data