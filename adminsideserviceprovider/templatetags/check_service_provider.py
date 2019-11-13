from django import template
from adminsideserviceprovider.models import ServiceProviderPlan,ServiceProviderCityMap
register = template.Library()


@register.assignment_tag()
def check_service_provider_func(id,city_id):
    if ServiceProviderCityMap.objects.filter(city_id=city_id,service_provider_id=id).exists():
       return 1
    else:
       return 0
 