from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap,TicketsCategories

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def ticket_list(request):
     if request.method == 'GET':

        tickets = CustomerTicketsCategoriesMap.objects.values('id',
                                                           'customer_id',
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
                                                           )

        tickets_cat = TicketsCategories.objects.values('id','category_title')

        return render(request, 'admin/ticket/ticketalldata/index.html',{'tickets':tickets,'tickets_cat':tickets_cat})
