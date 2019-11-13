from django import template
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap,TicketsCategoryWithServiceProvider

register = template.Library()

@register.simple_tag()
def get_tickets_category_count(pk):

    pendingCountTickets = CustomerTicketsCategoriesMap.objects.filter(ticketCategory_id=pk,working_status='Pending').count()

    return pendingCountTickets


@register.simple_tag()
def get_tickets_category_list(pk):

    ticketdata = TicketsCategoryWithServiceProvider.objects.values('id','ticket_category_id','service_provider_id','service_provider_id__service_provider_name').filter(ticket_category_id=pk)

    return ticketdata


@register.simple_tag()
def get_tickets_category_data_count(pk,cat_id):

    ticketdata = CustomerTicketsCategoriesMap.objects.filter(service_provider_id=pk,working_status='Pending',ticketCategory_id=cat_id).count()

    return ticketdata

@register.simple_tag()
def get_tickets_category_data_list(service_provider_id,ticketCategory_id):

    ticketdata = CustomerTicketsCategoriesMap.objects.values('id',
                                                           'customer_id','customer_id__first_name',
                                                           'customer_id','customer_id__last_name',
                                                           'customer_id','customer_id__account_id',
                                                           'ticketCategory_id',
                                                           'ticketCategory_id__category_title',
                                                           'service_provider_id',
                                                           'service_provider_id__service_provider_name',
                                                           'service_plan_hardware_id',
                                                           'subject',
                                                           'threads',
                                                           'category',
                                                           'priority',
                                                           'working_status',
                                                           'updatedby_id',
                                                           'updatedby_id__username',
                                                           'created_at',
                                                           'updated_at'
                                                           ).filter(service_provider_id=service_provider_id,ticketCategory_id=ticketCategory_id)

    return ticketdata