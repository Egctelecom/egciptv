from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import http.client
import json
import requests
from django.urls import reverse
from egciptvhome.models import CustomerApplyForService,CustomerApplyForServiceBilling
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage
from adminsidecustomer.models import Customer, AccountAddressCustomer, BillingAddressCustomer, \
    CutomerAttachmentMap, CustomerUserMap
from adminsidecustomer.models import City
from adminsidecustomer.models import Province
from adminsidecustomer.models import Country
from adminsideserviceprovider.models import ServiceProvider, CustomerWithService, CustomerServiceContract,Hardware,ServicePlanWithHardware,ContractbasedHardwarewithMAC
from crmadmin.models import UserProfile

def my_check(user):
    return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def apply_user(request):
    if request.method == 'GET':
        new_apply_service = CustomerApplyForService.objects.values('id','first_name','last_name','email_address','company_name','phone','cell_number')
        return render(request, 'admin/apply_users/index.html',{'new_apply_service':new_apply_service})


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def apply_user_profile(request,pk):
    if request.method == 'GET':
        
        new_apply_service_user = CustomerApplyForService.objects.values('id',
                                                                   'menu_category_id',
                                                                   'plan_id',
                                                                   'first_name',
                                                                   'last_name',
                                                                   'email_address',
                                                                   'company_name',
                                                                   'phone',
                                                                   'cell_number',
                                                                   'call_time',
                                                                   'installation_time',
                                                                   'hear_about_us',
                                                                   'existing_service_provider',
                                                                   'service_date_time',
                                                                   'cancellation_date_with_current_provider',
                                                                   'terms_of_service',
                                                                   'referred_ac_no',
                                                                   'referred_by',
                                                                   'message',
                                                                   'service_address_1',
                                                                   'service_address_2',
                                                                   'service_apt_suite',
                                                                   'service_city_id',
                                                                   'service_province_id',
                                                                   'service_country_id',
                                                                   'service_city_id__city_name',
                                                                   'service_province_id__province_name',
                                                                   'service_country_id__country_name',
                                                                   'service_postcode',
                                                                   'applied_ip_address',
                                                                   'previous_invoice',
                                                                   'created_at'
                                                                   ).filter(pk=pk)
        
        
        new_apply_service_user_billing = CustomerApplyForServiceBilling.objects.values('billing_address_1',
                                                                                       'billing_address_2',
                                                                                       'billing_apt_suite',
                                                                                       'billing_city_id',
                                                                                       'billing_province_id',
                                                                                       'billing_country_id',
                                                                                       'billing_postcode',
                                                                                       'billing_city_id__city_name',
                                                                                       'billing_province_id__province_name',
                                                                                       'billing_country_id__country_name',
                                                                                       ).filter(customer_apply_for_service_id=pk)

        
        return render(request, 'admin/apply_users/profile.html', {'new_apply_service_user': new_apply_service_user,
                                                                  'new_apply_service_user_billing':new_apply_service_user_billing
                                                                  })

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def send_mail_to_apply_user(request):
    if request.method=='POST':
        subject = 'A reply from Admin for your request to service plan'
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        to_email = request.POST['email_address']
        reply_message = request.POST['message']
        id = request.POST['id']
        
        massege = render_to_string('admin/apply_users/reply_mail.html',
                                   {'first_name': first_name, 'last_name': last_name,'reply_message':reply_message})
        
        html_msg = render_to_string('admin/apply_users/reply_mail.html',
                                    {'first_name': first_name, 'last_name': last_name, 'reply_message':reply_message})
        
        send_mail(subject, massege, 'support@25airport.com', [to_email], fail_silently=False, html_message=html_msg)
        
        messages.add_message(request, messages.SUCCESS,
                             'A reply mail successfully send to User')
        return HttpResponseRedirect(
            reverse('apply_user_profile', kwargs={'pk':id}))
    else:
        # messages.add_message(request, messages.ERROR, form.errors)
        return HttpResponseRedirect(
            reverse('apply_user_profile', kwargs={'pk':id}))
    
    
#=============================================================================================================================================================================================#


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def set_to_activated_users(request):
    if request.method=='GET':
    
            first_name = request.GET['first_name']
            last_name = request.GET['last_name']
            email = request.GET['email']
        
            if Customer.objects.filter(email_address=email).exists():
            
                return render(request, 'admin/apply_users/error.html')
    
            else:
        
                city = City.objects.values('id', 'city_name', 'province_id_id')
                province = Province.objects.values('id', 'province_name', 'country_id_id')
                country = Country.objects.values('id', 'country_name')
                service_provider = ServiceProvider.objects.values('id', 'service_provider_name')
                user_profile = UserProfile.objects.values('id', 'login_type', 'role', 'user_id__username')
         
                
                phone=request.GET['phone']
                cell_number=request.GET['cell_number']
                company_name=request.GET['company_name']
            
                billing_address_1=request.GET['billing_address_1']
                billing_address_2=request.GET['billing_address_2']
                billing_city_id=request.GET['billing_city_id']
                billing_province_id=request.GET['billing_province_id']
                billing_country_id=request.GET['billing_country_id']
                billing_postcode = request.GET['billing_postcode']
    
                address_1 = request.GET['address_1']
                address_2=request.GET['address_2']
                city_id=request.GET['account_city_id']
                province_id=request.GET['account_province_id']
                country_id=request.GET['account_country_id']
                account_postcode=request.GET['account_postcode']
    
                account_city_name =request.GET['account_city_name']
                account_province_name =request.GET['account_province_name']
                account_country_name =request.GET['account_country_name']
                billing_city_name =request.GET['billing_city_name']
                billing_province_name =request.GET['billing_province_name']
                billing_country_name =request.GET['billing_country_name']
    
               
    
                return render(request, 'admin/apply_users/add_to_activate_user.html', {
                                                                          'first_name': first_name,
                                                                          'last_name': last_name,
                                                                          'email': email,
                                                                          'phone': phone,
                                                                          'cell_number': cell_number,
                                                                          'company_name': company_name,
                                                                          'billing_address_1': billing_address_1,
                                                                          'billing_address_2': billing_address_2,
                                                                          'billing_city_id': billing_city_id,
                                                                          'billing_province_id': billing_province_id,
                                                                          'billing_country_id': billing_country_id,
                                                                          'address_1': address_1,
                                                                          'address_2': address_2,
                                                                          'city_id': city_id,
                                                                          'province_id': province_id,
                                                                          'country_id': country_id,
                                                                          'city': city,
                                                                          'province': province,
                                                                          'country': country,
                                                                          'service_provider': service_provider,
                                                                          'user_profile': user_profile,
                                                                          'account_postcode':account_postcode,
                                                                          'billing_postcode':billing_postcode,
                                                                          'account_city_name':account_city_name,
                                                                          'account_province_name':account_province_name,
                                                                          'account_country_name':account_country_name,
                                                                          'billing_city_name':billing_city_name,
                                                                          'billing_province_name':billing_province_name,
                                                                          'billing_country_name':billing_country_name
                                                                          })
    

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def set_to_user(request):
    if request.method=='POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        cell_number = request.POST['cell_number']
        company_name = request.POST['company_name']
    
        billing_address_1 = request.POST['billing_address_1']
        billing_address_2 = request.POST['billing_address_2']
        billing_city_id = request.POST['billing_city_id']
        billing_province_id = request.POST['billing_province_id']
        billing_country_id = request.POST['billing_country_id']
        billing_postcode = request.POST['billing_postcode']
    
        address_1 = request.POST['account_address_1']
        address_2 = request.POST['account_address_2']
        city_id = request.POST['account_city_id']
        province_id = request.POST['account_province_id']
        country_id = request.POST['account_country_id']
        account_postcode = request.POST['account_postcode']
    
        account_city_name = request.POST['account_city_name']
        account_province_name = request.POST['account_province_name']
        account_country_name = request.POST['account_country_name']
        billing_city_name = request.POST['billing_city_name']
        billing_province_name = request.POST['billing_province_name']
        billing_country_name = request.POST['billing_country_name']
        
        response_data = {}
        response_data['data'] = 'success'
        return JsonResponse(response_data, safe=False)
    
    
    

        