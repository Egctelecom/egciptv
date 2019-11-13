import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderPlan, CustomerWithService,CustomerServiceContract
from adminsideserviceprovider.templatetags.provider_functions import multipy
from crmadmin.models import ManageServicesPriceCategory, UserProfile
from django.contrib.auth.decorators import user_passes_test
from adminsidecustomer.models import Customer, AccountAddressCustomer, BillingAddressCustomer, BillingDetailsCustomer, \
    CutomerAttachmentMap,CustomerUserMap
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap,ServiceProviderCityMap
from django.urls import reverse
from adminnumberprovider.models import NumberProvinceCustomerMap

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add_user_service_price(request,id):
    if request.method == 'GET':
        array_of_id=[]
        customer_data = Customer.objects.values('id', 'account_id', 'status', 'first_name', 'first_name_gsr',
                                                'last_name', 'last_name_gsr', 'company_name', 'company_name_gsr',
                                                'portal_password', 'email_address', 'phone', 'other_phone', 'dob',
                                                'display_name', 'prefferd_language', 'zone').filter(pk=id)


        city = AccountAddressCustomer.objects.values('city_id').filter(user_id=id)
        city_service = ServiceProviderCityMap.objects.values('service_provider_id').filter(city_id=city[0]['city_id'])
        
        for city_services in city_service:
            array_of_id.append(city_services['service_provider_id'])
            
        services = ServiceProvider.objects.values('id','service_provider_name').filter(id__in=array_of_id)
        services_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status')
        services_provider_with_plan = ServiceProviderPlan.objects.values(
            'id',
            'service_provider_id__service_provider_name',
            'service_provider_id',
            'title',
            'retail',
            'actual',
            'qty'
        ).filter(service_provider_id__in=array_of_id)
        
        return render(request, 'admin/customer/add_service_plan.html',
                      {'servies_category': services_category,'customer_data':customer_data,'services':services,'services_provider_with_plan':services_provider_with_plan,'id':id})

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_service_plan(request):
    if request.is_ajax():
        service = request.POST['service']
        if service == 'not':
            services_provider_with_plan = ServiceProviderPlan.objects.values(
                'id',
                'service_provider_id__service_provider_name',
                'service_provider_id',
                'title',
                'retail',
                'actual',
                'qty'
            )
        else:
            services_provider_with_plan = ServiceProviderPlan.objects.values(
                'id',
                'title',
                'retail',
                'actual',
                'qty'
            ).filter(service_provider_id=service)

        data = render_to_string('admin/customer/list.html', {'services_provider_with_plan': services_provider_with_plan})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def changevalue(request):
    if request.is_ajax():
        actual = request.POST['actual']
        qty = request.POST['qty']
        data = multipy(actual,qty)
        response_data = {}
        response_data['actual'] = actual
        response_data['qty'] = qty
        response_data['data'] = data
        return JsonResponse(response_data, safe=False)

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def save_plan_to_user(request):
          if request.is_ajax():
              data = request.POST['data']
              actual = float(request.POST['actual'])
              qty = float(request.POST['qty'])
              retail = float(request.POST['retail'])
              user = request.POST['user']
              plan_paid_status = request.POST['plan_paid_status']

              provider= ServiceProviderPlan.objects.filter(pk=data).values('service_provider_id')

              if CustomerWithService.objects.filter(service_plan_id=data,user_id=user).exists():
                  response_data = {}
                  response_data['plan'] = data
                  response_data['success'] = 'false'
                  return JsonResponse(response_data, safe=False)
              else:
                  CustomerWithService.objects.create(
                      user_id=user,
                      service_provider_id=provider[0]['service_provider_id'],
                      service_plan_id=data,
                      plan_paid_status=plan_paid_status,
                      service_price_actual=actual,
                      service_price_retail=retail,
                      service_price_qty=qty
                  )
                  response_data = {}
                  response_data['plan'] = data
                  response_data['success'] = 'true'
                  return JsonResponse(response_data, safe=False)
              
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def delete_plan_to_user(request):
    pass


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit_customer_service_plan(request,pk):
    if request.method == 'GET':
        data = CustomerWithService.objects.values('id','user_id',
                      'service_provider_id__service_provider_name',
                      'service_plan_id__title',
                      'plan_paid_status',
                      'service_price_actual',
                      'service_price_retail',
                      'service_price_qty').filter(pk=pk)
        
        return render(request, 'admin/customer/edit_service_plan.html', {'data': data})
    
    if request.method == 'POST':
      if CustomerWithService.objects.filter(pk=pk).exists():
        customer_service = CustomerWithService.objects.get(pk=pk)
        customer_service.service_price_actual = request.POST['service_price_actual']
        customer_service.service_price_retail = request.POST['service_price_retail']
        customer_service.service_price_qty = request.POST['service_price_qty']
        customer_service.plan_paid_status = request.POST['plan_paid_status']
        customer_service.save()
        messages.add_message(request, messages.SUCCESS, 'Customer Service Plan added successfully')
        return HttpResponseRedirect(reverse('edit_customer_service_plan', kwargs={'pk': pk}))
    else:
        messages.add_message(request, messages.ERROR, form.errors)
        return HttpResponseRedirect(reverse('edit_customer_service_plan', kwargs={'pk': pk}))
        

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def delete_service_plan_to_user(request,pk):
    if request.method == 'GET':
        user = request.session['customer']
        if CustomerWithService.objects.filter(id=pk, user_id=user).exists():
            data = CustomerWithService.objects.get(id=pk, user_id=user)
            data.plan_status = 'N'
            data.save()

            customer_data = Customer.objects.values('id', 'account_id', 'status', 'first_name', 'first_name_gsr',
                                                    'last_name', 'last_name_gsr', 'company_name', 'company_name_gsr',
                                                    'portal_password', 'email_address', 'phone', 'other_phone', 'dob',
                                                    'display_name', 'prefferd_language', 'zone').filter(pk=user)
            service_plan = CustomerWithService.objects.values('id', 'service_plan_id__title', 'service_price_actual',
                                                              'service_price_retail', 'service_price_qty',
                                                              'plan_status').filter(user_id=user,plan_status='y')
            documents = CutomerAttachmentMap.objects.values('id', 'customer_id', 'filedata', 'file_type', 'file_name',
                                                            'created_at').filter(customer_id=customer_data[0]['id'])
            utickets = CustomerTicketsCategoriesMap.objects.values('id', 'customer_id', 'subject', 'threads', 'category',
                                                         'priority').filter(customer_id=customer_data[0]['id'], category='user')
            atickets = CustomerTicketsCategoriesMap.objects.values('id', 'customer_id', 'subject', 'threads', 'category',
                                                         'priority').filter(customer_id=customer_data[0]['id'], category='administrator')

            customer_plan_data = CustomerServiceContract.objects.values('id',
                                                                        'user_id',
                                                                        'customerwithservice'
                                                                        ).filter(user_id=user, type='New')

            customer_plan_data_terminate = CustomerServiceContract.objects.values('id',
                                                                                  'user_id',
                                                                                  'customerwithservice'
                                                                                  ).filter(user_id=user, type='Terminate')

            number_list = NumberProvinceCustomerMap.objects.values('number_id', 'number_id__did_id', 'number_id__number',
                                                                   'user_id__first_name', 'user_id__last_name',
                                                                   'updated_at').filter(user_id=user)
            return render(request, 'admin/users/details.html', {

                'customer': customer_data,
                'service_plan': service_plan,
                'documents': documents,
                'utickets': utickets,
                'atickets': atickets,
                'customer_plan_data': customer_plan_data,
                'customer_plan_data_terminate': customer_plan_data_terminate,
                'number_list': number_list

            })
