import base64
import datetime
import json
import random
from os import path

import pdfkit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.urls import reverse
from  settingcontractsheet.models import ContractSheet
from adminsidecustomer.models import Customer, AccountAddressCustomer
from adminsideserviceprovider.models import CustomerServiceContract, CustomerWithService, TerminateContractDetails,ServiceProviderPlan, ServicePlanWithHardware, Hardware,ContractbasedHardwarewithMAC
from pdf.utils import render_to_pdf
from django.contrib.auth.decorators import user_passes_test
from  adminsidecustomer.models import CustomerUserMap

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def create_new_contract(request,id):
    if request.method == 'GET':
        customer_services_plan = CustomerWithService.objects.values('user_id','service_provider_id','service_plan_id','service_plan_id__title','service_provider_id__service_provider_name','service_price_actual','service_price_retail','service_price_qty').filter(user_id=id,plan_status='y')
        return render(request, 'admin/customer/contract/add.html',{'id': id,'customer_services_plan':customer_services_plan})
    elif request.method == 'POST':
        customerwithserviceID = request.POST['customerwithservice']
        service_plan_hardware = request.POST['service_plan_hardware']
        contract_terms_data = request.POST['contract_terms_data']
        type = 'New'
        customerarray = json.dumps(customerwithserviceID)
        service_plan_hardwarearray = json.loads(service_plan_hardware)
        data  = CustomerServiceContract.objects.create(customerwithservice=customerarray,type=type,user_id=id,service_plan_hardware=service_plan_hardwarearray)
        data.contract_terms = contract_terms_data
        data.save()

        hw_array = []
        hw_list = []
        service_plan_with_hw_details = json.loads(service_plan_hardware)
        for hw in service_plan_with_hw_details:
            hw_array.append(hw)
        for hwdata in hw_array:
            if hwdata != '':
                data = ServicePlanWithHardware.objects.filter(pk=hwdata).values('hw_id')
                for DT in data:
                    hw_list.append(DT['hw_id'])

        for hwdata in hw_list:
            hw = Hardware.objects.values('id', 'hw_title', 'type', 'model', 'mac', 'sn', 'ver', 'usrn', 'passu',
                                         'adusr', 'adpass', 'dslusr',
                                         'dslpass', 'date_start', 'date_end', 'still_in_service', 'device_buy',
                                         'device_rental',
                                         'montly_rent').filter(pk=hwdata)
            data = ContractbasedHardwarewithMAC.objects.create(
                customer_id=id,
                hw_id=hw[0]['id'],
                type=hw[0]['type'],
                model=hw[0]['model'],
                mac=hw[0]['mac'],
                sn=hw[0]['sn'],
                ver=hw[0]['ver'],
                usrn=hw[0]['usrn'],
                passu=hw[0]['passu'],
                adusr=hw[0]['adusr'],
                adpass=hw[0]['adpass'],
                dslusr=hw[0]['dslusr'],
                dslpass=hw[0]['dslpass'],
                date_start=hw[0]['date_start'],
                date_end=hw[0]['date_end'],
                still_in_service=hw[0]['still_in_service'],
                device_buy=hw[0]['device_buy'],
                device_rental=hw[0]['device_rental'],
                montly_rent=hw[0]['montly_rent']
            )
        
        to_email = Customer.objects.values('first_name','last_name','email_address').filter(pk=id)
        subject = 'Contract of egciptv'

        AuthUserID = CustomerUserMap.objects.values('user_id').filter(customer_id=id)
        contract_data = ContractSheet.objects.values('title1',
                                                     'title2',
                                                     'title3',
                                                     'title4',
                                                     'title5',
                                                     'title6',
                                                     'title7',
                                                     'title8',
                                                     'title9',
                                                     'title10',
                                                     'title11',
                                                     'title12',
                                                     'title13',
                                                     'title14',
                                                     'title15',
                                                     'title16',
                                                     'title17').filter(user_id=AuthUserID[0]['user_id'])

        massege = render_to_string('admin/email.html',
                                   {'first_name': to_email[0]['first_name'], 'last_name': to_email[0]['last_name'],
                                    'contract_id': data.id})
        html_msg = render_to_string('admin/email.html',
                                    {'first_name': to_email[0]['first_name'], 'last_name': to_email[0]['last_name'],
                                     'contract_id': data.id})
        send_mail(subject, massege, 'support@25airport.com', [to_email[0]['email_address']], fail_silently=False,
                  html_message=html_msg)
        messages.add_message(request, messages.SUCCESS, 'Contract Added Successfully')
        return HttpResponseRedirect(reverse('create_new_contract', kwargs={'id': id}))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def terminate_contract(request,id):
    if request.method == 'GET':
        contract_date = datetime.datetime.now()
        return render(request, 'admin/customer/contract/teminate.html',{'id': id,'contract_date':contract_date})
    elif request.method == 'POST':
         cid = request.session['customer']
         contract = CustomerServiceContract.objects.create(user_id=cid,type='Terminate')
         contract.save()
         try:
            TerminateContractDetails.objects.create(customercontract_id=contract.id,
                                                 contract_type=request.POST['contract_type'],
                                                 contract_date=request.POST['contract_date'],
                                                 zone=request.POST['zone'],
                                                 monthly_charge=request.POST['monthly_charge'],
                                                 outstanding_balance=request.POST['outstanding_balance'],
                                                 cancellation_date=request.POST['cancellation_date'],
                                                 cancellation_charge=request.POST['cancellation_charge'],
                                                 admin_fee=request.POST['admin_fee'],
                                                 additional_charge=request.POST['additional_charge'],
                                                 comment=request.POST['comment']
                                                 )
         except KeyError:
             entry_title = "Guest"
             print(entry_title)

         to_email = Customer.objects.values('email_address','first_name','last_name').filter(pk=cid)
         subject = 'Contract of egciptv'
         massege = render_to_string('admin/terminateemail.html',
                                    {'first_name': to_email[0]['first_name'], 'last_name': to_email[0]['last_name'],'contract_id':contract.id})
         html_msg = render_to_string('admin/terminateemail.html',
                                     {'first_name': to_email[0]['first_name'], 'last_name': to_email[0]['last_name'],'contract_id':contract.id})
         send_mail(subject, massege, 'support@25airport.com', [to_email[0]['email_address']], fail_silently=False,
                   html_message=html_msg)
         messages.add_message(request, messages.SUCCESS, 'Your contract has been terminated')
         return HttpResponseRedirect(reverse('terminate_contract', kwargs={'id': cid}))

#========================================================== Get H/W according to service plan =====================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_hw_service_plan(request):
    if request.is_ajax():
        id = request.POST['service_plan']
        status = request.POST['status']
        if status == 'checked_value':
            service_plan_hw = ServicePlanWithHardware.objects.values('id','hw_id','hw_qty','hw_status','service_plan_id','hw_id__hw_title').filter(service_plan_id=id)
            arraylist = []
            for service_plan_hw_list in service_plan_hw:
                arraylist.append(service_plan_hw_list['id'])
            data = render_to_string('admin/customer/contract/hwlist/list.html', {'service_plan_hw': service_plan_hw})
            return HttpResponse(json.dumps({'data': data,'arraylist':arraylist}), content_type="application/json")
        else:
            j_id = json.loads(id)
            service_plan_hw_array=[]
            for jID in j_id:
                service_plan_hw = ServicePlanWithHardware.objects.values('id', 'hw_id', 'hw_qty', 'hw_status',
                                                                     'service_plan_id', 'hw_id__hw_title').filter(service_plan_id=jID)
                for service_planHw in service_plan_hw:
                    service_plan_hw_array.append(service_planHw['id'])
            
            arraylist = []
            for service_plan_hw_list in service_plan_hw_array:
                arraylist.append(service_plan_hw_list)
                
            data = render_to_string('admin/customer/contract/hwlist/list.html', {'service_plan_hw': service_plan_hw})
            return HttpResponse(json.dumps({'data': data, 'arraylist': arraylist}), content_type="application/json")
            


#================================================================================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def renew_contract(request,id):
   pass



@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def email_resend(request,id,contract_id):
    if request.method == 'GET':
        to_email = Customer.objects.values('email_address','first_name','last_name').filter(pk=id)
        subject = 'Contract of egciptv'
        massege = render_to_string('admin/email.html',{'first_name':to_email[0]['first_name'],'last_name':to_email[0]['last_name'],'contract_id':contract_id})
        html_msg = render_to_string('admin/email.html',{'first_name':to_email[0]['first_name'],'last_name':to_email[0]['last_name'],'contract_id':contract_id})
        send_mail(subject, massege, 'support@25airport.com', [to_email[0]['email_address']], fail_silently=False,
                  html_message=html_msg)
        id = request.session['customer']
        messages.add_message(request, messages.SUCCESS, 'Mail Resend')
        return HttpResponseRedirect(reverse('customer_details', kwargs={'id': id}))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def view_contract(request,id):
    if request.method == 'GET':
        request.session['contract_id'] = id
        customer_plan_data = CustomerServiceContract.objects.values(
            'id',
            'user_id',
            'customerwithservice',
            'service_plan_hardware',
            'type',
            'payment_status',
            'user_id__account_id',
            'user_id__first_name',
            'user_id__last_name',
            'user_id__email_address',
            'user_id__phone',
            'contract_terms',
            'created_at'
        ).filter(pk=id)
        address = AccountAddressCustomer.objects.values(
            'id',
            'user_id',
            'address_1',
            'address_2',
            'city__city_name',
            'province__province_name',
            'country__country_name'
            ).filter(user_id=customer_plan_data[0]['user_id'])
        n = random.randint(1000000, 9999999)

        # service_plan = CustomerWithService.objects.values('id', 'service_plan_id__title', 'service_price_actual',
        #                                                   'service_plan_id',
        #                                                   'service_price_retail', 'service_price_qty',
        #                                                   'plan_status').filter(user_id=customer_plan_data[0]['user_id'])
        total = 0
        arr = customer_plan_data[0]['customerwithservice']
        arr = arr.replace('"[', '')
        arr = arr.replace(']"', '')
        arr = arr.split(',')

        for ar in arr:
            service_plan = CustomerWithService.objects.values(
                'id',
                'service_plan_id__title',
                'service_price_actual',
                'service_price_retail',
                'service_price_qty',
                'plan_status'
            ).filter(service_plan_id=ar)
            ml = service_plan[0]['service_price_actual'] * service_plan[0]['service_price_qty']
            total = total + ml

        #=========================================================================================================================#

        totalhw = 0
        arrhwdata =[]
        for ar in arr:
            hardware = ServicePlanWithHardware.objects.values('id', 'hw_id', 'hw_qty', 'hw_status',
                                                              'hw_id__hw_title').filter(service_plan_id=ar)
            for hj in  hardware:
                arrhwdata.append(hj['hw_id'])
        array = []
        for h in arrhwdata:
            vale = Hardware.objects.values('device_buy').filter(pk=h)
            array.append(vale[0]['device_buy'])

        for hw in array:
            totalhw = totalhw + float(hw)
            
            
        AuthUserID = CustomerUserMap.objects.values('user_id').filter(customer_id=str(customer_plan_data[0]['user_id']))

        contract_data = ContractSheet.objects.values('title1',
                                            'title2',
                                            'title3',
                                            'title4',
                                            'title5',
                                            'title6',
                                            'title7',
                                            'title8',
                                            'title9',
                                            'title10',
                                            'title11',
                                            'title12',
                                            'title13',
                                            'title14',
                                            'title15',
                                            'title16',
                                            'title17').filter(user_id=AuthUserID[0]['user_id'])

        return render(request, 'admin/customer/contract/viewcontract.html',{
                       'id': id,
                       'customer_plan_data': customer_plan_data,
                       'hwDtata':json.loads(customer_plan_data[0]['service_plan_hardware']),
                       'contractData':arr,
                       'customerwithservicetotal':total,
                       'hw_total':totalhw,
                       'random_no':n,
                       'address':address,
                       'contract_terms':customer_plan_data[0]['contract_terms'],'contract_data':contract_data
                       })

# french
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def view_contract_french(request):
    if request.method == 'GET':
        id = request.session['contract_id']
        customer_plan_data = CustomerServiceContract.objects.values(
            'id',
            'user_id',
            'customerwithservice',
            'service_plan_hardware',
            'type',
            'payment_status',
            'user_id__account_id',
            'user_id__first_name',
            'user_id__last_name',
            'user_id__email_address',
            'user_id__phone',
            'created_at',
            'contract_terms'
        ).filter(pk=id)
        address = AccountAddressCustomer.objects.values(
            'id',
            'user_id',
            'address_1',
            'address_2',
            'city__city_name',
            'province__province_name',
            'country__country_name'
            ).filter(user_id=customer_plan_data[0]['user_id'])
        n = random.randint(1000000, 9999999)

        # service_plan = CustomerWithService.objects.values('id', 'service_plan_id__title', 'service_price_actual',
        #                                                   'service_plan_id',
        #                                                   'service_price_retail', 'service_price_qty',
        #                                                   'plan_status').filter(user_id=customer_plan_data[0]['user_id'])
        total = 0
        arr = customer_plan_data[0]['customerwithservice']
        arr = arr.replace('"[', '')
        arr = arr.replace(']"', '')
        arr = arr.split(',')

        for ar in arr:
            service_plan = CustomerWithService.objects.values(
                'id',
                'service_plan_id__title',
                'service_price_actual',
                'service_price_retail',
                'service_price_qty',
                'plan_status'
            ).filter(service_plan_id=ar)
            ml = service_plan[0]['service_price_actual'] * service_plan[0]['service_price_qty']
            total = total + ml

        #=========================================================================================================================#

        totalhw = 0
        arrhwdata =[]
        for ar in arr:
            hardware = ServicePlanWithHardware.objects.values('id', 'hw_id', 'hw_qty', 'hw_status',
                                                              'hw_id__hw_title').filter(service_plan_id=ar)
            for hj in  hardware:
                arrhwdata.append(hj['hw_id'])
        print(arrhwdata)
        array = []
        for h in arrhwdata:
            vale = Hardware.objects.values('device_buy').filter(pk=h)
            array.append(vale[0]['device_buy'])

        for hw in array:
            totalhw = totalhw + float(hw)

        return render(request, 'admin/customer/contract/viewcontractfrench.html',{
                       'id': id,
                       'customer_plan_data': customer_plan_data,
                       'hwDtata':json.loads(customer_plan_data[0]['service_plan_hardware']),
                       'contractData':arr,
                       'customerwithservicetotal':total,
                       'hw_total':totalhw,
                       'random_no':n,
                       'address':address,
                       'contract_terms': customer_plan_data[0]['contract_terms']
                       })

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def email_contract(request,id):
    if request.method == 'GET':
        customer_plan_data = CustomerServiceContract.objects.values(
            'id',
            'user_id',
            'customerwithservice',
            'type',
            'payment_status',
            'user_id__account_id',
            'user_id__first_name',
            'user_id__last_name',
            'user_id__email_address',
            'created_at',
            'contract_terms'
        ).filter(pk=id)
        address = AccountAddressCustomer.objects.values(
            'id',
            'user_id',
            'address_1',
            'address_2',
            'city__city_name',
            'province__province_name',
            'country__country_name'
            ).filter(user_id=customer_plan_data[0]['user_id'])

        subject = 'Contract of egciptv'

        n = random.randint(1000000, 9999999)

        service_plan = CustomerWithService.objects.values('id', 'service_plan_id__title', 'service_price_actual',
                                                          'service_plan_id',
                                                          'service_price_retail', 'service_price_qty',
                                                          'plan_status').filter(
            user_id=customer_plan_data[0]['user_id'])

        service_plan_hardware = ServicePlanWithHardware.objects.values('id', 'hw_id', 'hw_qty', 'hw_status',
                                                                       'hw_id__hw_title').filter(
            service_plan_id=service_plan[0]['service_plan_id'])

        # file_path = path.relpath("r/download.pdf")
        # f = open(file_path, 'w+')
        # ty = render_to_string('admin/customer/contract/mail/contract_attch.html')
        # f.write(ty)
        # f.close()

        pdf = render_to_string('admin/customer/contract/mail/email.html')
        file_path = path.relpath("r/contract.pdf")
        fd = open(file_path, 'rb')
        msg = EmailMessage(subject,pdf,'support@25airport.com', to=[request.GET['emailto']])
        msg.attach("contract.pdf", fd.read(), 'application/pdf')
        msg.content_subtype = "html"
        msg.encoding = 'utf-8'
        msg.send()

        id = request.session['customer']
        messages.add_message(request, messages.SUCCESS, 'Mail Resend')
        return HttpResponseRedirect(reverse('customer_details', kwargs={'id': id}))



#===================================================================== PAYMENT ===================================================================
def go_for_payment(request,id):
    customer_plan_data = CustomerServiceContract.objects.values('id',
                                                                'user_id',
                                                                'customerwithservice',
                                                                'type',
                                                                'payment_status').filter(pk=id)
    
    print(customer_plan_data)
    service_plan = CustomerWithService.objects.values('id',
                                                      'service_plan_id__title',
                                                      'service_price_actual',
                                                      'service_plan_id',
                                                      'service_price_retail',
                                                      'service_price_qty',
                                                      'plan_status').filter(user_id=customer_plan_data[0]['user_id'])

    hardware = ServicePlanWithHardware.objects.values('id',
                                                      'hw_id',
                                                      'hw_qty',
                                                      'hw_status',
                                                      'hw_id__hw_title').filter(service_plan_id=service_plan[0]['service_plan_id'])
    array=[]
    for h in hardware:
        vale = Hardware.objects.values('device_buy').filter(pk=h['hw_id'])
        array.append(vale[0]['device_buy'])
    n = random.randint(1000, 9999)
    total = 0
    for hw in array:
      total = total + float(hw)
    total = total + service_plan[0]['service_price_actual']

    return render(request, 'admin/customer/contract/payment.html',
                  {'id': id,'service_plan':total,'random_no':n})