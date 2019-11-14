from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
import json
import requests
from django.views.generic.base import View

from adminnumberprovider.models import NumberProvinceCustomerMap,NumberMNPtoCustomer
from crmadmin.models import CallCost
from adminsidecustomer.forms import Customerform
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from adminsidecustomer.models import Customer, AccountAddressCustomer, BillingAddressCustomer, BillingDetailsCustomer, \
    CutomerAttachmentMap, CustomerUserMap, Sales_tax
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap
from adminsidecustomer.models import City
from adminsidecustomer.models import Province
from adminsidecustomer.models import Country
from adminsidecustomer.models import CustomerAccountStatus
from adminsideserviceprovider.models import ServiceProvider, CustomerWithService, CustomerServiceContract,Hardware,ServicePlanWithHardware,ContractbasedHardwarewithMAC
from crmadmin.models import UserProfile
from adminsidecustomer.forms import ContractbasedHardwareform
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.core.mail import send_mail
from adminnumberprovider.templatetags.check_number_functions import is_number_plus,check_number,check_number2,is_rate_code_chart_plus,cost,plus_cost
from datetime import datetime

import io
import base64
def my_check(user):
    return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def index(request):
    if request.method == 'GET':
        customer_data = CustomerUserMap.objects.values('customer_id','user_id',
                                                       'customer_id__id',
                                                       'customer_id__account_id',
                                                       'customer_id__status',
                                                       'customer_id__first_name',
                                                       'customer_id__first_name_gsr',
                                                       'customer_id__last_name',
                                                       'customer_id__last_name_gsr',
                                                       'customer_id__company_name',
                                                       'customer_id__company_name_gsr',
                                                       'customer_id__portal_password',
                                                       'customer_id__email_address',
                                                       'customer_id__phone',
                                                       'customer_id__other_phone',
                                                       'customer_id__dob',
                                                       'customer_id__display_name',
                                                       'customer_id__prefferd_language',
                                                       'customer_id__zone',
                                                       'customer_id__created_at'
                                                       )
        
        for i in customer_data:
            i['monthly'] = 0
            plans = CustomerWithService.objects.filter(user_id=i['customer_id'])
            for j in plans:
                i['monthly'] += j.service_price_retail
            
        return render(request, 'admin/users/index.html', {'customer': customer_data})



@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def change_password(request,pk):
    if request.method=='GET':
        return render(request,'admin/users/change_password.html',{'pk':pk})
    elif request.method=='POST':
        
        new_password = request.POST['new_password']
        new_cnf_password = request.POST['new_cnf_password']
        
        if new_password==new_cnf_password:
            
            if User.objects.filter(pk=pk).exists:
                
                user_details = User.objects.values('first_name', 'last_name','email').filter(pk=pk)
                customer = CustomerUserMap.objects.values('user_id', 'customer_id').filter(user_id=pk)
                
                cus = Customer.objects.get(pk=customer[0]['customer_id'])
                cus.portal_password = new_password
                cus.save()
                
                user_data = User.objects.get(pk=pk)
                user_data.set_password(new_password)
                user_data.save()
                
                
                msg = 'Your Password be changed'
                subject = 'Any further query please contact to admin '
                
                massege = render_to_string('admin/email_template/customer_password.html',
                                           {'first_name': user_details[0]['first_name'],
                                            'last_name': user_details[0]['last_name'],
                                            'msg': msg,
                                            'portal_password': new_password
                                            })
                
                html_msg = render_to_string('admin/email_template/customer_password.html',
                                            {'first_name': user_details[0]['first_name'],
                                             'last_name': user_details[0]['last_name'],
                                             'msg': msg,
                                             'portal_password': new_password
                                             })
                
                # send_mail(subject, massege, 'support@25airport.com', [user_details[0]['email']],
                #           fail_silently=False, html_message=html_msg)
                
                messages.add_message(request, messages.SUCCESS, 'Password updated successfully')
                return HttpResponseRedirect(reverse('change_password', kwargs={'pk': pk}))
            
            else:
                
                messages.add_message(request, messages.SUCCESS, 'User not exits')
                return HttpResponseRedirect(reverse('change_password', kwargs={'pk': pk}))
        
        
        else:
            messages.add_message(request, messages.SUCCESS, 'Password should be same')
            return HttpResponseRedirect(reverse('change_password',kwargs={'pk':pk}))




@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add(request):
    if  request.method == 'GET':
        city = City.objects.values('id', 'city_name', 'province_id_id')
        province = Province.objects.values('id', 'province_name', 'country_id_id')
        country = Country.objects.values('id', 'country_name')
        service_provider = ServiceProvider.objects.values('id','service_provider_name')
        user_profile = UserProfile.objects.values('id','login_type','role','user_id__username')
        return render(request, 'admin/users/add.html',{'city':city,'province':province,'country':country,'service_provider':service_provider,'user_profile':user_profile})
    elif request.method == 'POST':
        form = Customerform(request.POST)
        if form.is_valid():
            user = form.save()
            if Customer.objects.filter(pk=user.id).exists:
                
                if 'year_pre_payment' not in request.POST:
                    year_pre_payment = False
                else:
                    year_pre_payment = request.POST['year_pre_payment']
                
                data = User.objects.create(username=request.POST['first_name'],
                                           first_name = request.POST['first_name'],
                                           last_name = request.POST['last_name'],
                                           email = request.POST['email_address'],
                                           )
                data.set_password(request.POST['portal_password'])
                data.save()
                
                CustomerUserMap.objects.create(user_id=data.id,
                                               customer_id = user.id
                                               )
                AccountAddressCustomer.objects.create(user_id=user.id,
                                                      address_1=request.POST['address_1'],
                                                      address_2 = request.POST['address_2'] ,
                                                      city_id = request.POST['city'],
                                                      province_id = request.POST['province'],
                                                      country_id = request.POST['country'],
                                                      postal=request.POST['postal']
                                                      )
                BillingAddressCustomer.objects.create(user_id=user.id,
                                                      billing_address_1=request.POST['billing_address_1'],
                                                      billing_address_2 = request.POST['billing_address_2'] ,
                                                      billing_city_id = request.POST['billing_city'],
                                                      billing_province_id = request.POST['billing_province'],
                                                      billing_country_id = request.POST['billing_country'],
                                                      postal=request.POST['billing_postal']
                                                      )
                
                # BillingDetailsCustomer.objects.create(user_id=user.id,
                #                                       salesperson_id=request.POST['salesperson'],
                #                                       contract_type = request.POST['contract_type'] ,
                #                                       billing_day = request.POST['billing_day'],
                #                                       payment_mode = request.POST['payment_mode'],
                #                                       payment_method = request.POST['payment_method'],
                #                                       year_pre_payment = year_pre_payment,
                #                                       billing_from = request.POST['billing_from'],
                #                                       billing_to = request.POST['billing_to']
                #                                       )
                
                # Send Mail function is truned off
                msg = 'Your account created'
                subject = 'Customer Account of egciptv'
                massege = render_to_string('admin/email_template/customer_data_mail.html',{'first_name': request.POST['first_name'], 'last_name': request.POST['last_name'],'msg':msg,'portal_password':request.POST['portal_password']})
                html_msg = render_to_string('admin/email_template/customer_data_mail.html',{'first_name': request.POST['first_name'],'last_name': request.POST['last_name'],'msg':msg,'portal_password': request.POST['portal_password']})
                # send_mail(subject, massege, 'support@25airport.com', [request.POST['email_address']], fail_silently=False,html_message=html_msg)
                
                messages.add_message(request, messages.SUCCESS, 'Customer added successfully')
                return HttpResponseRedirect(reverse('add_customer'))
            else:
                messages.add_message(request, messages.SUCCESS, 'Customer not create successfully')
                return HttpResponseRedirect(reverse('add_customer'))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('add_customer'))


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit(request, id):
    if request.method == 'GET':
        customer_data = Customer.objects.filter(pk=id)
        account_address = AccountAddressCustomer.objects.filter(user_id=id)
        billing_address = BillingAddressCustomer.objects.filter(user_id=id)
        # billing_details = BillingDetailsCustomer.objects.filter(user_id=id)
        
        province = Province.objects.values('id', 'province_name')
        city = City.objects.values('id', 'city_name')
        country = Country.objects.values('id', 'country_name')
        
        service_provider = ServiceProvider.objects.values('id', 'service_provider_name')
        user_profile = UserProfile.objects.values('id', 'login_type', 'role', 'user_id__username')
        return render(request, 'admin/users/edit.html', {
            'customer':customer_data,
            'account_address':account_address,
            'billing_address':billing_address,
            # 'billing_details':billing_details,
            'province':province,
            'city':city,
            'country':country,
            'service_provider':service_provider,
            'user_profile':user_profile
        })
    elif request.method == 'POST':
        data = Customer.objects.get(pk=id)
        form = Customerform(request.POST)
        if form.is_valid():
            if request.POST['need_password'] == 'true':
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
            else:
                data.first_name = form['first_name'].data
                data.last_name = form['last_name'].data
                data.first_name_gsr = form['first_name_gsr'].data
                data.last_name = form['last_name'].data
                data.last_name_gsr = form['last_name_gsr'].data
                data.company_name_gsr = form['company_name_gsr'].data
                data.company_name = form['company_name'].data
                data.email_address = form['email_address'].data
                data.phone = form['phone'].data
                data.other_phone = form['other_phone'].data
                data.dob = form['dob'].data
                data.display_name = form['display_name'].data
                data.prefferd_language = form['prefferd_language'].data
                data.zone = form['zone'].data
                data.save()
            
            customerdata = CustomerUserMap.objects.values('user_id').filter(customer_id=id)
            userdata = User.objects.values('first_name').filter(pk=customerdata[0]['user_id'])
            user = User.objects.get(pk=customerdata[0]['user_id'])
            success = user.check_password(request.POST['portal_password'])
            
            account_address = AccountAddressCustomer.objects.get(user_id=id)
            account_address.address_1 = request.POST['address_1']
            account_address.address_2 = request.POST['address_2']
            account_address.city_id = request.POST['city']
            account_address.province_id = request.POST['province']
            account_address.country_id = request.POST['country']
            account_address.postal = request.POST['postal']
            account_address.save()
            
            billing_address = BillingAddressCustomer.objects.get(user_id=id)
            billing_address.billing_address_1 = request.POST['billing_address_1']
            billing_address.billing_address_2 = request.POST['billing_address_2']
            billing_address.billing_city_id = request.POST['billing_city']
            billing_address.billing_province_id = request.POST['billing_province']
            billing_address.billing_country_id = request.POST['billing_country']
            billing_address.postal = request.POST['billing_postal']
            billing_address.save()
            
        
        
        if request.POST['first_name'] != userdata[0]['first_name']:
            
            msg = 'Your account username be updated'
            subject = 'Customer Account of egciptv'
            massege = render_to_string('admin/email_template/customer_data_mail.html',
                                       {
                                           'first_name': request.POST['first_name'],
                                           'last_name': request.POST['last_name'],
                                           'portal_password': request.POST['portal_password'],
                                           'msg':msg
                                       })
            html_msg = render_to_string('admin/email_template/customer_data_mail.html',
                                        {
                                            'first_name': request.POST['first_name'],
                                            'last_name': request.POST['last_name'],
                                            'portal_password': request.POST['portal_password'],
                                            'msg': msg
                                        })
            # send_mail(subject, massege, 'support@25airport.com', [request.POST['email_address']], fail_silently=False,
            #           html_message=html_msg)
            #
        elif success:
            print (success)
        else:
            
            msg = 'Your account password be updated'
            subject = 'Customer Account of egciptv'
            massege = render_to_string('admin/email_template/customer_data_mail.html',
                                       {
                                           'first_name': request.POST['first_name'],
                                           'last_name': request.POST['last_name'],
                                           'portal_password': request.POST['portal_password'],
                                           'msg': msg
                                       })
            html_msg = render_to_string('admin/email_template/customer_data_mail.html',
                                        {
                                            'first_name': request.POST['first_name'],
                                            'last_name': request.POST['last_name'],
                                            'portal_password': request.POST['portal_password'],
                                            'msg': msg
                                        })
            # send_mail(subject, massege, 'support@25airport.com', [request.POST['email_address']],
            #           fail_silently=False,
            #           html_message=html_msg)
        
        
        messages.add_message(request, messages.SUCCESS, 'Customer Update successfully')
        return HttpResponseRedirect(reverse('edit_customer', kwargs={'id': id}))
    else:
        # messages.add_message(request, messages.ERROR, form.errors)
        return HttpResponseRedirect(reverse('edit_customer', kwargs={'id': id}))

#=========================================================== Customer Details Page =====================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def details(request, id):
    if request.method == 'GET':
        request.session['customer']=id
        customer_data = Customer.objects.values('id','account_id','status','first_name','first_name_gsr','last_name','last_name_gsr','company_name','company_name_gsr','portal_password','email_address','phone','other_phone','dob','display_name','prefferd_language','zone').filter(pk=id)
        service_plan = CustomerWithService.objects.values('id','service_plan_id__title','service_price_actual','service_price_retail','service_price_qty','plan_status','plan_paid_status').filter(user_id=id,plan_status='y')
        monthly_total = 0
        for i in service_plan:
            monthly_total += i['service_price_actual']
        province = BillingAddressCustomer.objects.get(user__id=customer_data[0]['id']).billing_province
        tax_rate = Sales_tax.objects.get(province=province)
        
        tax = monthly_total * tax_rate.tax_rate / 100
        total_charge = tax + monthly_total
        documents = CutomerAttachmentMap.objects.values('id','customer_id','filedata','file_type','file_name','created_at').filter(customer_id=id)
        utickets = CustomerTicketsCategoriesMap.objects.values('id','customer_id','subject','threads','category','priority').filter(customer_id=id,category='user')
        atickets = CustomerTicketsCategoriesMap.objects.values('id','customer_id','subject','threads','category','priority').filter(customer_id=id,category='administrator')
        
        total_tickets = len(utickets) + len(atickets)
        customer_plan_data = CustomerServiceContract.objects.values('id',
                                                                    'user_id',
                                                                    'customerwithservice'
                                                                    ).filter(user_id=id,type='New')
        # print(customer_plan_data.count())
        
        customer_plan_data_terminate = CustomerServiceContract.objects.values('id',
                                                                              'user_id',
                                                                              'customerwithservice'
                                                                              ).filter(user_id=id, type='Terminate')
        
        #-------hardware details of each customer--------------------------------------------------------------------------#
        
        if CustomerServiceContract.objects.filter(user_id=id,type='New').exists():
            service_plan_with_hw_details = CustomerServiceContract.objects.values('id',
                                                                                  'user_id',
                                                                                  'customerwithservice','service_plan_hardware'
                                                                                  ).filter(user_id=id,type='New')
            
            
            
            
            
            hw_array=[]
            # for hw in service_plan_with_hw_details:
            #     customerServiceContracthw = hw['service_plan_hardware']
            #     customerServiceContracthw = customerServiceContracthw.replace('[', '')
            #     customerServiceContracthw = customerServiceContracthw.replace(']', '')
            #     hw_array.append(customerServiceContracthw)
            
            hw_list =[]
            hw_list_id=[]
            service_plan_with_hw_details = json.loads(service_plan_with_hw_details[0]['service_plan_hardware'])
            for hw in service_plan_with_hw_details:
                hw_array.append(hw)
            for hwdata in hw_array:
                if hwdata != '':
                    data = ServicePlanWithHardware.objects.filter(pk=hwdata).values('hw_id')
                    for DT in data:
                        hw_list.append(DT['hw_id'])
            
            
            hw_list_title = []
            hw_list_type = []
            hw_list_device_buy = []
            hw_list_device_rental = []
            hw_list_montly_rent = []
            
            data_array_title =[]
            data_array_type =[]
            data_array_id =[]
            data_array_device_buy =[]
            data_array_device_rental =[]
            data_array_montly_rent =[]
            contarct_based_hw_id=[]
            for hwdata in hw_list:
                data = ContractbasedHardwarewithMAC.objects.filter(hw_id=hwdata,customer_id=id).values(
                    'id',
                    'hw_id__hw_title',
                    'hw_id',
                    'type',
                    'model',
                    'mac',
                    'sn','ver','usrn','passu','adusr','adpass','dslusr',
                    'dslpass','date_start','date_end', 'still_in_service','device_buy','device_rental',
                    'montly_rent')
                
                for dtt in data:
                    data_array_title.append(dtt['hw_id__hw_title'])
                    contarct_based_hw_id.append(dtt['id'])
                    data_array_id.append(dtt['hw_id'])
                    data_array_type.append(dtt['type'])
                    data_array_device_buy.append(dtt['device_buy'])
                    data_array_device_rental.append(dtt['device_rental'])
                    data_array_montly_rent.append(dtt['montly_rent'])
            
            for dt in data_array_title:
                hw_list_title.append(dt)
            
            for dt in data_array_type:
                hw_list_type.append(dt)
            
            for dt in data_array_device_buy:
                hw_list_device_buy.append(dt)
            
            for dt in data_array_device_rental:
                hw_list_device_rental.append(dt)
            
            for dt in data_array_montly_rent:
                hw_list_montly_rent.append(dt)
            
            for dt in data_array_id:
                hw_list_id.append(dt)
        else:
            hw_list_title = []
            hw_list_type = []
            hw_list_device_buy = []
            hw_list_device_rental = []
            hw_list_montly_rent = []
            hw_list_id=[]
            contarct_based_hw_id=[]
        
        
        number_list = NumberProvinceCustomerMap.objects.values('number_id','number_id__did_id','number_id__number','user_id__first_name','user_id__last_name','user_id__id','updated_at').filter(user_id=id).order_by('updated_at')
        port_number_list = NumberMNPtoCustomer.objects.values('id','user_id__id','updated_at','number','approve_upload_data').filter(user_id=id).order_by('updated_at')
        return render(request, 'admin/users/details.html',{
            
            'customer':customer_data,
            'service_plan':service_plan,
            'documents':documents,
            'utickets':utickets,
            'atickets':atickets,
            'customer_plan_data':customer_plan_data,
            'customer_plan_data_terminate':customer_plan_data_terminate,
            'number_list':number_list,
            'hw_list_title':hw_list_title,
            'hw_list_type':hw_list_type,
            'hw_list_device_buy':hw_list_device_buy,
            'hw_list_montly_rent':hw_list_montly_rent,
            'hw_list_device_rental':hw_list_device_rental,
            'hw_list_id':hw_list_id,
            'port_number_list':port_number_list,
            'contarct_based_hw_id':contarct_based_hw_id,
            'monthly_total': monthly_total,
            'tax': tax,
            'tax_rate': tax_rate,
            'total_charge': total_charge,
            'total_tickets': total_tickets
        })




@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def customer_delete(request,pk):
    if request.method == 'GET':
        if CustomerUserMap.objects.filter(customer_id=pk).exists():
            customer_obj = CustomerUserMap.objects.get(customer_id=pk)
            User.objects.filter(id=customer_obj.user.id).delete()
            Customer.objects.filter(id=customer_obj.customer.id).delete()
            customer_obj.delete()
    return HttpResponseRedirect(reverse('customer'))
    # id = CustomerUserMap.objects.values('user_id').filter(customer_id=pk)
    # request.session['myid'] = id[0]['user_id']
    # CustomerUserMap.objects.filter(customer_id=pk).delete()
    # if User.objects.filter(id=pk).exists():
    #  User.objects.filter(pk=request.session['myid']).delete()
    #  if Customer.objects.filter(pk=pk).exixts():
    #      Customer.objects.filter(pk=pk).delete()
    
    # customer_data = CustomerUserMap.objects.values('customer_id', 'user_id',
    #                                                'customer_id__id',
    #                                                'customer_id__account_id',
    #                                                'customer_id__status',
    #                                                'customer_id__first_name',
    #                                                'customer_id__first_name_gsr',
    #                                                'customer_id__last_name',
    #                                                'customer_id__last_name_gsr',
    #                                                'customer_id__company_name',
    #                                                'customer_id__company_name_gsr',
    #                                                'customer_id__portal_password',
    #                                                'customer_id__email_address',
    #                                                'customer_id__phone',
    #                                                'customer_id__other_phone',
    #                                                'customer_id__dob',
    #                                                'customer_id__display_name',
    #                                                'customer_id__prefferd_language',
    #                                                'customer_id__zone',
    #                                                'customer_id__created_at'
    #                                                )
    # return render(request, 'admin/users/index.html', {'customer': customer_data})


#================================================================= Customer contract with mac address of each h/w for each user ===========================================================================

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def view_hw_MAC(request,pk,customer_pk,id):
    if request.method == 'GET':
        hw_data = ContractbasedHardwarewithMAC.objects.values('id', 'hw_id','customer_id','hw_id__hw_title','type','model','mac','sn','ver','usrn','passu','adusr','adpass','dslusr',
                                                              'dslpass','date_start','date_end', 'still_in_service','device_buy','device_rental',
                                                              'montly_rent').filter(hw_id=pk,customer_id=customer_pk,pk=id)
        
        data = Hardware.objects.values('id', 'hw_title', 'type', 'model', 'mac', 'sn', 'ver', 'usrn',
                                       'passu', 'adusr', 'adpass', 'dslusr',
                                       'dslpass', 'date_start', 'date_end', 'still_in_service',
                                       'device_buy', 'device_rental',
                                       'montly_rent').filter(pk=pk)
        
        return render(request, 'admin/users/hw/view.html', {'hw_data': hw_data,'pk':pk,'customer_pk':customer_pk,'data':data,'id':id})


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit_hw_MAC(request,pk,customer_pk,id):
    if request.method =='POST':
        if ContractbasedHardwarewithMAC.objects.filter(hw_id=pk,customer_id=customer_pk,pk=id).exists():
            data = ContractbasedHardwarewithMAC.objects.get(hw_id=pk,customer_id=customer_pk,pk=id)
            form = ContractbasedHardwareform(request.POST)
            if form.is_valid():
                data.type = form['type'].data
                data.model = form['model'].data
                data.mac = form['mac'].data
                data.sn = form['sn'].data
                data.ver = form['ver'].data
                data.usrn = form['usrn'].data
                data.passu = form['passu'].data
                data.adusr = form['adusr'].data
                data.adpass = form['adpass'].data
                data.dslusr = form['dslusr'].data
                data.dslpass = form['dslpass'].data
                data.date_start = form['date_start'].data
                data.date_end = form['date_end'].data
                data.still_in_service = form['still_in_service'].data
                data.device_buy = form['device_buy'].data
                data.device_rental = form['device_rental'].data
                data.montly_rent = form['montly_rent'].data
                data.save()
                messages.add_message(request, messages.SUCCESS, 'Contract Hardware with MAC edited ')
                return HttpResponseRedirect(reverse('view_hw_MAC', kwargs={'pk': pk,'customer_pk':customer_pk,'id':id}))
            else:
                messages.add_message(request, messages.ERROR, form.errors)
                return HttpResponseRedirect(reverse('view_hw_MAC', kwargs={'pk': pk,'customer_pk':customer_pk,'id':id}))
        else:
            form = ContractbasedHardwareform(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Contract Hardware with MAC edited ')
                return HttpResponseRedirect(reverse('view_hw_MAC', kwargs={'pk': pk, 'customer_pk': customer_pk,'id':id}))
            else:
                messages.add_message(request, messages.ERROR, form.errors)
                return HttpResponseRedirect(reverse('view_hw_MAC', kwargs={'pk': pk, 'customer_pk': customer_pk,'id':id}))

#================================================================= Customer number mnp to our provider =====================================================================================================

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def port_number(request,customer_pk):
    if request.method == 'GET':
        customer_data = CustomerUserMap.objects.filter(customer_id=customer_pk).values('customer_id', 'user_id',
                                                                                       'customer_id__id',
                                                                                       'customer_id__account_id',
                                                                                       'customer_id__status',
                                                                                       'customer_id__first_name',
                                                                                       'customer_id__first_name_gsr',
                                                                                       'customer_id__last_name',
                                                                                       'customer_id__last_name_gsr',
                                                                                       'customer_id__company_name',
                                                                                       'customer_id__company_name_gsr',
                                                                                       'customer_id__portal_password',
                                                                                       'customer_id__email_address',
                                                                                       'customer_id__phone',
                                                                                       'customer_id__other_phone',
                                                                                       'customer_id__dob',
                                                                                       'customer_id__display_name',
                                                                                       'customer_id__prefferd_language',
                                                                                       'customer_id__zone',
                                                                                       'customer_id__created_at'
                                                                                       )
        return render(request, 'admin/users/mnp_set.html', {'customer_pk':customer_pk,'customer_data':customer_data})


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def save_port_number(request):
    if request.is_ajax():
        mobile_number = request.POST['mobile_number']
        customer_pk = request.POST['customer_pk']
        approve_upload_data = request.POST['approve_upload_data_base64']
        url = "https://apiv1.teleapi.net/lnp/check"
        querystring = {"token": "73ad3b26-88a2-4f59-90ae-9be6a256782d",
                       "numbers": mobile_number}
        payload = ""
        headers = {
            'cache-control': "no-cache",
            'Postman-Token': "ac92ca24-3d5b-4d47-8fa6-a57b2fed168f"
        }
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        check_data = response.json()
        status = check_data["data"][mobile_number]["status"]
        message = check_data["data"][mobile_number]["message"]
        response_data = {}
        if status == 'success':
            NumberMNPtoCustomer.objects.create(number=mobile_number,user_id=customer_pk,approve_upload_data=approve_upload_data)
            response_data['data']='success'
        else:
            response_data['data']='error'
        return JsonResponse(response_data, safe=False)


# @login_required(login_url="/admin")
# @user_passes_test(my_check,login_url='/admin')
# def set_mnp(request,customer_pk):
#     if request.method == 'POST':
#         mobile_no =  request.POST['mobile_no']
#         customer_data = CustomerUserMap.objects.filter(customer_id=customer_pk).values('customer_id', 'user_id',
#                                                        'customer_id__id',
#                                                        'customer_id__account_id',
#                                                        'customer_id__status',
#                                                        'customer_id__first_name',
#                                                        'customer_id__first_name_gsr',
#                                                        'customer_id__last_name',
#                                                        'customer_id__last_name_gsr',
#                                                        'customer_id__company_name',
#                                                        'customer_id__company_name_gsr',
#                                                        'customer_id__portal_password',
#                                                        'customer_id__email_address',
#                                                        'customer_id__phone',
#                                                        'customer_id__other_phone',
#                                                        'customer_id__dob',
#                                                        'customer_id__display_name',
#                                                        'customer_id__prefferd_language',
#                                                        'customer_id__zone',
#                                                        'customer_id__created_at'
#                                                        )
#         url = "https://apiv1.teleapi.net/lnp/check"
#         querystring = {"token": "73ad3b26-88a2-4f59-90ae-9be6a256782d",
#                         "numbers": mobile_no}
#         payload=""
#         headers = {
#             'cache-control': "no-cache",
#             'Postman-Token': "ac92ca24-3d5b-4d47-8fa6-a57b2fed168f"
#         }
#         response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
#         check_data = response.json()
#         status = check_data["data"][mobile_no]["status"]
#         message = check_data["data"][mobile_no]["message"]
#         return render(request, 'admin/users/mnp_set.html', {'mobile_no': mobile_no,'customer_pk':customer_pk,'status':'success','message':message,'customer_data':customer_data})

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def set_mnp_add(request):
    numbers = request.POST['numbers']
    location_type = request.POST['location_type']
    account_number = request.POST['account_number']
    service_address = request.POST['service_address']
    service_city = request.POST['service_city']
    service_state = request.POST['service_state']
    service_zip = request.POST['service_zip']
    btn = request.POST['btn']
    partial_port = request.POST['partial_port']
    wireless_pin = request.POST['wireless_pin']
    caller_id = request.POST['caller_id']
    bill_file_base64 = 'hjjhvj'
    signature_base64 = 'hjhghj'
    url = "https://apiv1.teleapi.net/lnp/create"
    if location_type == 'business' :
        business_contact = request.POST['business_contact']
        business_name = request.POST['business_name']
        querystring = {"token": "73ad3b26-88a2-4f59-90ae-9be6a256782d", "numbers": numbers,
                       "location_type": location_type, "business_contact": business_contact, "business_name": business_name,
                       "account_number": account_number, "service_address": service_address,"bill_file":bill_file_base64,
                       "service_city": service_city,"wireless_pin":wireless_pin,"caller_id":caller_id,"signature":signature_base64,
                       "service_state": service_state, "service_zip": service_zip, "btn": btn, "partial_port": partial_port,
                       "wireless_number": "0"}
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        querystring = {"token": "73ad3b26-88a2-4f59-90ae-9be6a256782d", "numbers": numbers,
                       "location_type": location_type, "first_name": first_name, "last_name": last_name,
                       "account_number": account_number, "service_address": service_address,"bill_file":bill_file_base64,
                       "service_city": service_city,"wireless_pin":wireless_pin,"caller_id":caller_id,"signature":signature_base64,
                       "service_state": service_state, "service_zip": service_zip, "btn": btn, "partial_port": partial_port,
                       "wireless_number": "0"}
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "ac92ca24-3d5b-4d47-8fa6-a57b2fed168f"
    }
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    check_data = response.json()
    messages.info(request, 'somthing problem on mnp.')
    return HttpResponseRedirect(reverse('set_mnp',))



#==============================================CDR Records==============================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def cdr_number_records(request,number,customer_id):
    
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y")
    
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "ac92ca24-3d5b-4d47-8fa6-a57b2fed168f"
    }
    payload = ""
    url2 = "https://cdr.teleapi.net/cdr/"+date_time+"/"+date_time+"?token=73ad3b26-88a2-4f59-90ae-9be6a256782d"
    response2 = requests.request("GET", url2, data=payload, headers=headers)
    data = response2.text
    date_gmt = []
    source = []
    destination = []
    callerid = []
    hangup_code = []
    sip_account = []
    orig_ip = []
    duration = []
    per_minute = []
    callcost = []
    type = []
    uuid = []
    data_array = data.split('\r\n')
    i = 0
    for i in range(len(data_array) - 1):
        if i > 0:
            row_data = data_array[i].split(',')
            date_gmt.append(row_data[0])
            source.append(str(row_data[1])[-10:])
            destination.append(row_data[2])
            callerid.append(row_data[3])
            hangup_code.append(row_data[4])
            sip_account.append(row_data[5])
            orig_ip.append(row_data[6])
            duration.append(row_data[7])
            per_minute.append(row_data[8])
            callcost.append(row_data[9])
            type.append(row_data[10])
            uuid.append(row_data[11])
        i = i + 1
    start_date = date_time
    end_date = date_time
    
    user_id = CustomerUserMap.objects.values('user_id').filter(customer_id=customer_id)
    i=0
    for date in destination:
        
        if number == source[i] or number == destination[i]:
            
            IS_PLUS = is_number_plus(date)
            
            if IS_PLUS=='+':
                
                IS_PLUS_CHECK_NUMBER = check_number(date)
                RATE_PLUS = is_rate_code_chart_plus(IS_PLUS_CHECK_NUMBER)
                c = plus_cost(RATE_PLUS,duration[i])
                if CallCost.objects.filter(user_id=user_id[0]['user_id'],source=source[i],destination=destination[i],start_date=start_date,end_date=end_date).exists():
                    
                    
                    print('hi')
                
                else:
                    
                    CallCost.objects.create(user_id=user_id[0]['user_id'],source=source[i],destination=destination[i],call_cost=c,start_date=start_date,end_date=end_date)
            
            else:
                
                IS_CHECK_NUMBER = check_number2(date)
                RATE = is_rate_code_chart_plus(IS_CHECK_NUMBER)
                c  = cost(RATE,duration[i])
                
                if CallCost.objects.filter(user_id=user_id[0]['user_id'], source=source[i], destination=destination[i],
                                           start_date=start_date, end_date=end_date).exists():
                    print('hi')
                
                else:
                    
                    CallCost.objects.create(user_id=user_id[0]['user_id'], source=source[i], destination=destination[i],
                                            call_cost=c, start_date=start_date, end_date=end_date)
            
            i = i+1
    
    return render(request, 'admin/cdr/index.html',
                  {'date_gmt': date_gmt, 'source': source, 'destination': destination, 'callerid': callerid,
                   'hangup_code': hangup_code, 'sip_account': sip_account,
                   'orig_ip': orig_ip, 'duration': duration, 'per_minute': per_minute, 'callcost': callcost,
                   'type': type, 'uuid': uuid,'start_date': start_date,
                   'end_date': end_date,'number':number})


#============================================ user billaddress same as account address ==================================#
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def same_as_account_address(request):
    if request.is_ajax():
        province = Province.objects.values('id', 'province_name').filter(country_id_id=request.POST['country'])
        city = City.objects.values('id', 'city_name').filter(province_id_id=request.POST['province'])
        data = render_to_string('admin/users/listdata.html', {'province': province,
                                                              'city': city,
                                                              'city_id': request.POST['city'] ,
                                                              'province_id' : request.POST['province']
                                                              })
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")




#============================================ Change Account status of Customer ==================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def change_account_status_of_customer(request):
    if request.is_ajax():
        if CustomerAccountStatus.objects.filter(customer_id=request.POST['id']).exists():
            customer = CustomerAccountStatus.objects.get(customer_id=request.POST['id'])
            customer.contract_sent=request.POST['contract_sent']
            customer.contract_accepted=request.POST['contract_accepted']
            customer.first_payment_done=request.POST['first_payment_done']
            customer.req_has_been_sent=request.POST['req_has_been_sent']
            customer.devices_shipped=request.POST['devices_shipped']
            customer.devices_received=request.POST['devices_received']
            customer.installation_date=request.POST['installation_date']
            customer.installation_done=request.POST['installation_done']
            customer.save()
        
        else:
            CustomerAccountStatus.objects.create(customer_id=request.POST['id'],
                                                 contract_sent = request.POST['contract_sent'],
                                                 contract_accepted = request.POST['contract_accepted'],
                                                 first_payment_done = request.POST['first_payment_done'],
                                                 req_has_been_sent = request.POST['req_has_been_sent'],
                                                 devices_shipped = request.POST['devices_shipped'],
                                                 devices_received = request.POST['devices_received'],
                                                 installation_date = request.POST['installation_date'],
                                                 installation_done = request.POST['installation_done'])
        
        
        response_data = {}
        if CustomerAccountStatus.objects.filter(customer_id=request.POST['id']).exists():
            customer = CustomerAccountStatus.objects.values('customer_id',
                                                            'contract_sent',
                                                            'contract_accepted',
                                                            'first_payment_done',
                                                            'req_has_been_sent',
                                                            'devices_shipped',
                                                            'devices_received',
                                                            'installation_date',
                                                            'installation_done').filter(customer_id=request.POST['id'])
            
            if customer[0]['contract_sent'] == 'False' and customer[0]['contract_accepted'] == 'False' and customer[0]['first_payment_done'] == 'False' and customer[0]['req_has_been_sent']== 'False' and customer[0]['devices_shipped']== 'False' and customer[0]['devices_received']== 'False' and customer[0]['installation_date']== 'False' and customer[0]['installation_date']== 'False' and customer[0]['installation_done']== 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status ='0%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '0'
                return JsonResponse(response_data, safe=False)
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'False' and customer[0]['first_payment_done'] == 'False' and customer[0]['req_has_been_sent'] == 'False' and customer[0]['devices_shipped'] == 'False' and customer[0]['devices_received']== 'False' and customer[0]['installation_date'] == 'False' and customer[0]['installation_done'] == 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '12.5%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '12.5%'
                return JsonResponse(response_data, safe=False)
            
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'True' and customer[0]['first_payment_done'] == 'False' and customer[0]['req_has_been_sent'] == 'False' and customer[0]['devices_shipped'] == 'False' and customer[0]['devices_received']== 'False' and customer[0]['installation_date'] == 'False' and customer[0]['installation_done'] == 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '25%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '25%'
                return JsonResponse(response_data, safe=False)
            
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'True' and customer[0]['first_payment_done'] == 'True' and customer[0]['req_has_been_sent'] == 'False' and customer[0]['devices_shipped'] == 'False' and customer[0]['devices_received']== 'False' and customer[0]['installation_date'] == 'False' and customer[0]['installation_done'] == 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '37.5%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '37.5%'
                return JsonResponse(response_data, safe=False)
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'True' and customer[0]['first_payment_done'] == 'True' and customer[0]['req_has_been_sent'] == 'True' and customer[0]['devices_shipped'] == 'False' and customer[0]['devices_received']== 'False' and customer[0]['installation_date'] == 'False' and customer[0]['installation_done'] == 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '50%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '50%'
                return JsonResponse(response_data, safe=False)
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'True' and customer[0]['first_payment_done'] == 'True' and customer[0]['req_has_been_sent'] == 'True' and customer[0]['devices_shipped'] == 'True'  and customer[0]['devices_received']== 'False' and customer[0]['installation_date'] == 'False' and customer[0]['installation_done'] == 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '62.5%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '62.5%'
                return JsonResponse(response_data, safe=False)
            
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'True' and customer[0]['first_payment_done'] == 'True' and customer[0]['req_has_been_sent'] == 'True' and customer[0]['devices_shipped'] == 'True' and customer[0]['devices_received']== 'True' and customer[0]['installation_date'] == 'False' and customer[0]['installation_done'] == 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '75%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '75%'
                return JsonResponse(response_data, safe=False)
            
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'True' and customer[0]['first_payment_done'] == 'True' and customer[0]['req_has_been_sent'] == 'True' and customer[0]['devices_shipped'] == 'True' and customer[0]['devices_received']== 'True' and customer[0]['installation_date'] == 'True' and customer[0]['installation_done'] == 'False':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '87.5%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '87.5%'
                return JsonResponse(response_data, safe=False)
            
            elif customer[0]['contract_sent'] == 'True' and customer[0]['contract_accepted'] == 'True' and customer[0]['first_payment_done'] == 'True' and customer[0]['req_has_been_sent'] == 'True' and customer[0]['devices_shipped'] == 'True' and customer[0]['devices_received']== 'True' and customer[0]['installation_date'] == 'True' and customer[0]['installation_done'] == 'True':
                
                cutUser = Customer.objects.get(pk=request.POST['id'])
                cutUser.status = '100%'
                cutUser.save()
                
                response_data['data'] = 'success'
                response_data['account_status'] = '100%'
                return JsonResponse(response_data, safe=False)
        
                
def send_password_mail(request, pk):
    if request.is_ajax():
        # print(pk)
        # print(request.POST['new_password'])
        # Send mail

        msg = 'Your Password has been changed'
        subject = 'Any further query please contact to admin '
        user_details = User.objects.values('first_name', 'last_name', 'email').filter(pk=pk)
        customer = CustomerUserMap.objects.values('user_id', 'customer_id').filter(user_id=pk)

        massege = render_to_string('admin/email_template/customer_password.html',
                                   {'first_name': user_details[0]['first_name'],
                                    'last_name': user_details[0]['last_name'],
                                    'msg': msg,
                                    'portal_password': request.POST['new_password']
                                    })

        html_msg = render_to_string('admin/email_template/customer_password.html',
                                    {'first_name': user_details[0]['first_name'],
                                     'last_name': user_details[0]['last_name'],
                                     'msg': msg,
                                     'portal_password': request.POST['new_password']
                                     })

        send_mail(subject, massege, 'support@25airport.com', [user_details[0]['email']],
                  fail_silently=False, html_message=html_msg)
        
        return JsonResponse(data={
            'state': True,
            'message': "Success"
        }, status=200)


def send_password_sms(request, pk):
    if request.is_ajax():
        # print(pk)
        # print(request.POST['new_password'])
        # Send mail
        
        msg = 'Your Password has been changed'
        subject = 'Any further query please contact to admin '
        user_details = User.objects.values('first_name', 'last_name', 'email').filter(pk=pk)
        customer = CustomerUserMap.objects.values('user_id', 'customer_id').filter(user_id=pk)
        
        massege = render_to_string('admin/email_template/customer_password.html',
                                   {'first_name': user_details[0]['first_name'],
                                    'last_name': user_details[0]['last_name'],
                                    'msg': msg,
                                    'portal_password': request.POST['new_password']
                                    })
        
        html_msg = render_to_string('admin/email_template/customer_password.html',
                                    {'first_name': user_details[0]['first_name'],
                                     'last_name': user_details[0]['last_name'],
                                     'msg': msg,
                                     'portal_password': request.POST['new_password']
                                     })
        
        # send sms
        
        return JsonResponse(data={
            'state': True,
            'message': "Success"
        }, status=200)



class SendCustomMail(View):
    def get(self, request, pk):
        customer_obj = Customer.objects.get(id=pk)
        return render(request, 'admin/users/custom_email.html', {'customer_obj': customer_obj})
    
    def post(self, request, pk):
        customer_obj = Customer.objects.get(id=pk)
        message = request.POST['message']
        
        #send Mail
        
        messages.success(request, "Mail Sent")
        return HttpResponseRedirect(reverse('customer_custom_mail', kwargs={'pk': pk}))
            
            
            
            
          
            
          

        
