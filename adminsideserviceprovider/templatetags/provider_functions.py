from django import template
from adminsideserviceprovider.models import ServiceProviderPlan
register = template.Library()

@register.simple_tag()
def multipy(qty,price):
    data = float(price)*float(qty)
    return data

@register.simple_tag()
def get_service_provider(id):
    services_provider_with_plan = ServiceProviderPlan.objects.values('id', 'manage_service_category_id',
                                                                     'service_provider_id__service_provider_name',
                                                                     'service_provider_id', 'title', 'retail', 'actual',
                                                                     'qty').filter(manage_service_category_id=id)
    return services_provider_with_plan

