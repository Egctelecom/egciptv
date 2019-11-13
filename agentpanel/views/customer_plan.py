import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from adminsidecustomer.models import Customer
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderPlan, CustomerWithService
from adminsideserviceprovider.templatetags.provider_functions import multipy
from crmadmin.models import ManageServicesPriceCategory, UserProfile
from django.contrib.auth.decorators import user_passes_test
from agentpanel.models import Agent

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def add_user_service_price(request,id):
    if request.method == 'GET':
        customer_data = Customer.objects.values('id', 'account_id', 'status', 'first_name', 'first_name_gsr',
                                                'last_name', 'last_name_gsr', 'company_name', 'company_name_gsr',
                                                'portal_password', 'email_address', 'phone', 'other_phone', 'dob',
                                                'display_name', 'prefferd_language', 'zone').filter(pk=id)
        services = ServiceProvider.objects.values('id','service_provider_name')
        services_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status')
        services_provider_with_plan = ServiceProviderPlan.objects.values(
            'id',
            'service_provider_id__service_provider_name',
            'service_provider_id',
            'title',
            'retail',
            'actual',
            'qty'
        )
        return render(request, 'agent/customer/add_service_plan.html',
                      {'servies_category': services_category,'customer_data':customer_data,'services':services,'services_provider_with_plan':services_provider_with_plan,'id':id})

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def get_service_plan(request):
    if request.is_ajax():
        service = request.POST['service']
        print(service)
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
            print(services_provider_with_plan)
        else:
            services_provider_with_plan = ServiceProviderPlan.objects.values(
                'id',

                'title',
                'retail',
                'actual',
                'qty'
            ).filter(service_provider_id=service)

        data = render_to_string('agent/customer/list.html', {'services_provider_with_plan': services_provider_with_plan})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
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

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def save_plan_to_user(request):
          if request.is_ajax():
              data = request.POST['data']
              actual = float(request.POST['actual'])
              qty = float(request.POST['qty'])
              retail = float(request.POST['retail'])
              user = request.POST['user']

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
                      service_price_actual=actual,
                      service_price_retail=retail,
                      service_price_qty=qty
                  )
                  response_data = {}
                  response_data['plan'] = data
                  response_data['success'] = 'true'
                  return JsonResponse(response_data, safe=False)
@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def delete_plan_to_user(request):
    pass
