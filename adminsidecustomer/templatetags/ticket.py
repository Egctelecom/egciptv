import json

from django import template

from adminsideserviceprovider.models import ServicePlanWithHardware

register = template.Library()

@register.simple_tag()
def get_hw(id):
    data = ServicePlanWithHardware.objects.values('id','hw_id__hw_title', 'service_plan', 'service_plan_id__title',
                                                  'hw_id').filter(hw_id=id)

    return data[0]['hw_id__hw_title']


