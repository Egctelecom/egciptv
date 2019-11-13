from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from adminnumberprovider.models import NumberProvinceCustomerMap
from adminsidecustomer.forms import Customerform
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from adminsidecustomer.models import Customer, AccountAddressCustomer, BillingAddressCustomer, BillingDetailsCustomer, \
    CutomerAttachmentMap
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap
from adminsidecustomer.models import City
from adminsidecustomer.models import Province
from adminsidecustomer.models import Country
from adminsideserviceprovider.models import ServiceProvider, CustomerWithService, CustomerServiceContract
from crmadmin.models import UserProfile
from django.contrib.auth.decorators import user_passes_test
from agentpanel.models import Agent

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def index(request):
 if request.method == 'GET':
    customer_data = Customer.objects.all()
    return render(request, 'agent/users/index.html',{'customer':customer_data})

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def add(request):
 if  request.method == 'GET':
     city = City.objects.values('id', 'city_name', 'province_id_id')
     province = Province.objects.values('id', 'province_name', 'country_id_id')
     country = Country.objects.values('id', 'country_name')
     service_provider = ServiceProvider.objects.values('id','service_provider_name')
     user_profile = UserProfile.objects.values('id','login_type','role','user_id__username')
     return render(request, 'agent/users/add.html',{'city':city,'province':province,'country':country,'service_provider':service_provider,'user_profile':user_profile})
 elif request.method == 'POST':
    form = Customerform(request.POST)
    if form.is_valid():
        user = form.save()
        if Customer.objects.filter(pk=user.id).exists:
            AccountAddressCustomer.objects.create(user_id=user.id,
                                                  address_1=request.POST['address_1'],
                                                  address_2 = request.POST['address_2'] ,
                                                  city_id = request.POST['city'],
                                                  province_id = request.POST['province'],
                                                  country_id = request.POST['country']
                                                  )
            BillingAddressCustomer.objects.create(user_id=user.id,
                                                  billing_address_1=request.POST['billing_address_1'],
                                                  billing_address_2 = request.POST['billing_address_2'] ,
                                                  billing_city_id = request.POST['billing_city'],
                                                  billing_province_id = request.POST['billing_province'],
                                                  billing_country_id = request.POST['billing_country']
                                                  )
            BillingDetailsCustomer.objects.create(user_id=user.id,
                                                  salesperson_id=request.POST['salesperson'],
                                                  contract_type = request.POST['contract_type'] ,
                                                  billing_day = request.POST['billing_day'],
                                                  payment_mode = request.POST['payment_mode'],
                                                  payment_method = request.POST['payment_method'],
                                                  year_pre_payment = request.POST['year_pre_payment'],
                                                  billing_from = request.POST['billing_from'],
                                                  billing_to = request.POST['billing_to']
                                                  )
            messages.add_message(request, messages.SUCCESS, 'Customer added successfully')
            return HttpResponseRedirect(reverse('agent_add_customer'))
        else:
            messages.add_message(request, messages.SUCCESS, 'Customer not create successfully')
            return HttpResponseRedirect(reverse('add_customer'))
    else:
        messages.add_message(request, messages.ERROR, form.errors)
        return HttpResponseRedirect(reverse('agent_add_customer'))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def edit(request,id):
 if  request.method == 'GET':
     customer_data = Customer.objects.values('id','account_id','status','first_name','first_name_gsr','last_name','last_name_gsr','company_name','company_name_gsr','portal_password','email_address','phone','other_phone','dob','display_name','prefferd_language','zone').filter(pk=id)
     return render(request, 'agent/users/edit.html',{'customer':customer_data})
 elif request.method == 'POST':
        data = Customer.objects.get(pk=id)
        form = Customerform(request.POST)
        if form.is_valid():
            data.first_name = form['first_name'].data
            data.last_name = form['last_name'].data
            data.first_name_gsr = form['first_name_gsr'].data
            data.last_name = form['last_name'].data
            data.last_name_gsr = form['last_name_gsr'].data
            data.company_name_gsr = form['company_name_gsr'].data
            data.company_name = form['company_name'].data
            data.email_address = form['email_address'].data
            data.phone = form['phone'].data
            data.portal_password = form['portal_password'].data
            data.other_phone = form['other_phone'].data
            data.dob = form['dob'].data
            data.display_name = form['display_name'].data
            data.prefferd_language = form['prefferd_language'].data
            data.zone = form['zone'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Customer Update successfully')
            return HttpResponseRedirect(reverse('agent_edit_customer', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_edit_customer', kwargs={'id': id}))

#=========================================================== Customer Details Page =========================================

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def details(request,id):
 if  request.method == 'GET':
     request.session['customer']=id
     customer_data = Customer.objects.values('id','account_id','status','first_name','first_name_gsr','last_name','last_name_gsr','company_name','company_name_gsr','portal_password','email_address','phone','other_phone','dob','display_name','prefferd_language','zone').filter(pk=id)
     service_plan = CustomerWithService.objects.values('id','service_plan_id__title','service_price_actual','service_price_retail','service_price_qty','plan_status').filter(user_id=id)
     documents = CutomerAttachmentMap.objects.values('id','customer_id','filedata','file_type','file_name','created_at').filter(customer_id=id)
     utickets = CustomerTicketsCategoriesMap.objects.values('id','customer_id','subject','threads','category','priority').filter(customer_id=id,category='user')
     atickets = CustomerTicketsCategoriesMap.objects.values('id','customer_id','subject','threads','category','priority').filter(customer_id=id,category='administrator')

     customer_plan_data = CustomerServiceContract.objects.values('id',
                                                                 'user_id',
                                                                 'customerwithservice'
                                                                 ).filter(user_id=id,type='New')

     customer_plan_data_terminate = CustomerServiceContract.objects.values('id',
                                                                 'user_id',
                                                                 'customerwithservice'
                                                                 ).filter(user_id=id, type='Terminate')

     number_list = NumberProvinceCustomerMap.objects.values('number_id','number_id__did_id','number_id__number','user_id__first_name','user_id__last_name','updated_at').filter(user_id=id)
     return render(request, 'agent/users/details.html',{

         'customer':customer_data,
         'service_plan':service_plan,
         'documents':documents,
         'utickets':utickets,
         'atickets':atickets,
         'customer_plan_data':customer_plan_data,
         'customer_plan_data_terminate':customer_plan_data_terminate,
         'number_list':number_list

     })
