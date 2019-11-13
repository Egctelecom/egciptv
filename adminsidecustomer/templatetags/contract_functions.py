import json

from django import template

from adminsideserviceprovider.models import CustomerWithService, Hardware, ServicePlanWithHardware

register = template.Library()

@register.simple_tag()
def get_contract_name(array):
    service_array=[]
    for arr in array:
         service_plan = CustomerWithService.objects.values(
                                                      'id',
                                                      'service_plan_id__title',
                                                      'service_price_actual',
                                                      'service_price_retail',
                                                      'service_price_qty',
                                                      'plan_status'
                                                       ).filter(service_plan_id=arr)
         service_array.append(service_plan['0']['service_plan_id__title'])

    return service_array

@register.simple_tag()
def get_hw(service_plan_id):
    hardware = ServicePlanWithHardware.objects.values('id','hw_id','hw_qty','hw_status','hw_id__hw_title').filter(service_plan_id=service_plan_id)
    array=[]
    for h in hardware:
        vale = Hardware.objects.values('device_buy').filter(pk=h['hw_id'])
        array.append(vale[0]['device_buy'])
    total = 0
    for hw in array:
        total = total + float(hw)
    return total

@register.simple_tag()
def get_hw_price(id):
    vale = Hardware.objects.values('device_buy').filter(pk=id)
    return vale[0]['device_buy']

@register.simple_tag()
def total_price(a,b):
    total = 0
    total = total + float(a) + float(b)
    return total


@register.simple_tag()
def get_hw_title_details(id):
    hardware = ServicePlanWithHardware.objects.values('id','hw_id','hw_qty','hw_status','hw_id__hw_title','hw_id__device_buy').filter(id=id)
    return hardware[0]['hw_id__hw_title']

@register.simple_tag()
def get_hw_qty_details(id):
    hardware = ServicePlanWithHardware.objects.values('id','hw_id','hw_qty','hw_status','hw_id__hw_title','hw_id__device_buy').filter(id=id)
    return hardware[0]['hw_qty']

@register.simple_tag()
def get_hw_price_details(id):
    hardware = ServicePlanWithHardware.objects.values('id','hw_id','hw_qty','hw_status','hw_id__hw_title','hw_id__device_buy').filter(id=id)
    return hardware[0]['hw_id__device_buy']


@register.simple_tag()
def get_contract_title_details(id):
    print(id)
    service_plan = CustomerWithService.objects.values(
        'id',
        'service_plan_id__title',
        'service_price_actual',
        'service_price_retail',
        'service_price_qty',
        'plan_status'
    ).filter(service_plan_id=id)
    return service_plan[0]['service_plan_id__title']

@register.simple_tag()
def get_contract_price_details(id):
    service_plan = CustomerWithService.objects.values(
        'id',
        'service_plan_id__title',
        'service_price_actual',
        'service_price_retail',
        'service_price_qty',
        'plan_status'
    ).filter(service_plan_id=id)
    return service_plan[0]['service_price_actual']


@register.simple_tag()
def get_contract_qty_details(id):
    service_plan = CustomerWithService.objects.values(
        'id',
        'service_plan_id__title',
        'service_price_actual',
        'service_price_retail',
        'service_price_qty',
        'plan_status'
    ).filter(service_plan_id=id)
    return service_plan[0]['service_price_qty']

@register.simple_tag()
def subtotal_contract_price(a,b):
    total = 0;
    total = total + (float(a)*float(b))
    return total


@register.simple_tag()
def subtotal_hw_price(a,b):
    total = 0;
    total = total + (float(a) * float(b))
    return total


@register.simple_tag()
def fulltotal(a,b):
    total = 0;
    total = total + float(a) + float(b)
    return total
