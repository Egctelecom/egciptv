from apscheduler.schedulers.blocking import BlockingScheduler
from django.template.loader import render_to_string
from django.core.mail import send_mail

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "egciptv.settings")
django.setup()

import requests
from adminnumberprovider.models import NumberMNPtoCustomer
from adminsidecustomer.models import Customer,CustomerUserMap
from adminnumberprovider.templatetags.check_number_functions import is_number_plus,check_number,check_number2,is_rate_code_chart_plus,cost,plus_cost
from adminsideserviceprovider.models import CustomerServiceContract
from ratecustomerbillingwithcdr.models import CustomerBillingDetails
from crmadmin.models import CallCost
from datetime import datetime
import json


from adminsideserviceprovider.models import CustomerServiceContract, CustomerWithService, TerminateContractDetails,ServiceProviderPlan, ServicePlanWithHardware, Hardware,ContractbasedHardwarewithMAC
from adminsidecustomer.models import Customer, AccountAddressCustomer

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=24*60)
def timed_job():
    customer_list  = Customer.objects.values('id','first_name','last_name','email_address')
    for cus in customer_list:
        payment_details = CustomerServiceContract.objects.values('id','payment_status').filter(user_id=cus['id'])
        print(payment_details[0]['payment_status'])
        if payment_details[0]['payment_status'] == 'Pending':
            subject = 'Payment Service Provider , Egciptv'
            massege = 'You are payment till now | Please Payment your service price'
            html_msg = render_to_string('admin/email.html',{'first_name': cus['first_name'], 'last_name': cus['last_name'],'contract_id': payment_details[0]['id']})
            send_mail(subject, massege, 'support@25airport.com', [cus['email_address']],fail_silently=False,html_message=html_msg)
            
@sched.scheduled_job('interval', minutes=24*60)
def billing_job():
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y")

    customer_list  = Customer.objects.values('id','first_name','last_name','email_address')
    for cus in customer_list:
        num = NumberMNPtoCustomer.objects.filter(user_id=cus['id']).first()
        number = num.number
        print(num.number)
        print(num)

        headers = {
            'cache-control': "no-cache",
            'Postman-Token': "ac92ca24-3d5b-4d47-8fa6-a57b2fed168f"
        }
        payload = ""
        url2 = "https://cdr.teleapi.net/cdr/"+date_time+"/"+date_time+"?token=73ad3b26-88a2-4f59-90ae-9be6a256782d"
        # url2 = "https://cdr.teleapi.net/cdr/01-01-2018/07-12-2018?token=73ad3b26-88a2-4f59-90ae-9be6a256782d"
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

        # start_date = '01-01-2018'
        # end_date = '07-12-2018'

        start_date = date_time
        end_date = date_time


        user_id = CustomerUserMap.objects.values('user_id').filter(customer_id=cus['id'])
        i = 0
        for date in destination:

            if number == date:

                IS_PLUS = is_number_plus(date)

                if IS_PLUS == '+':

                    IS_PLUS_CHECK_NUMBER = check_number(date)
                    RATE_PLUS = is_rate_code_chart_plus(IS_PLUS_CHECK_NUMBER)
                    c = plus_cost(RATE_PLUS, duration[i])
                    if CallCost.objects.filter(user_id=user_id[0]['user_id'], source=source[i],
                                               destination=destination[i], start_date=start_date,
                                               end_date=end_date).exists():

                        print('hi')

                    else:

                        CallCost.objects.create(user_id=user_id[0]['user_id'], source=source[i],
                                                destination=destination[i], call_cost=c, start_date=start_date,
                                                end_date=end_date)

                else:

                    IS_CHECK_NUMBER = check_number2(date)
                    RATE = is_rate_code_chart_plus(IS_CHECK_NUMBER)
                    c = cost(RATE, duration[i])

                    if CallCost.objects.filter(user_id=user_id[0]['user_id'], source=source[i],
                                               destination=destination[i],
                                               start_date=start_date, end_date=end_date).exists():
                        print('')

                    else:

                        CallCost.objects.create(user_id=user_id[0]['user_id'], source=source[i],
                                                destination=destination[i],
                                                call_cost=c, start_date=start_date, end_date=end_date)

                i = i + 1


@sched.scheduled_job('interval',  minutes=24*60)
def create_bill():
    customer_list = Customer.objects.values('id', 'first_name', 'last_name', 'email_address')

    contract = []
    callcost = []
    CustomerPlanData = []
    HwDtata = []
    Arr = []
    Total = []
    Totalhw = []
    for cus in customer_list:

        address = AccountAddressCustomer.objects.values(
            'id',
            'user_id',
            'address_1',
            'address_2',
            'city__city_name',
            'province__province_name',
            'country__country_name'
        ).filter(user_id=cus['id'])

        contract_list = CustomerServiceContract.objects.values('id', 'customerwithservice', 'type',
                                                               'service_plan_hardware').filter(user_id=cus['id'],payment_status='Pending',type='New')
        for cl in contract_list:
            contract.append(cl['id'])

        user = CustomerUserMap.objects.filter(customer_id=cus['id']).first()
        if user:
            call_cost_list = CallCost.objects.values('id', 'call_cost').filter(user_id=user.user_id,
                                                                               start_date__gte='01-01-2018',
                                                                               start_date__lte='10-01-2018')
            for cl in call_cost_list:
                callcost.append(cl['id'])

        if user:

            billing_details = CustomerBillingDetails.objects.create(user_id=user.user_id,
                                                                    customer_service_contract=json.dumps(contract),
                                                                    call_cost=json.dumps(callcost),
                                                                    payment_status='Pending')

            # ================================================================================= Contract List================================================================================================#

            customerServiceContract = json.loads(billing_details.customer_service_contract)

            for csc in customerServiceContract:
                id = csc
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

                CustomerPlanData.append(customer_plan_data)
                HwDtata.append(customer_plan_data[0]['service_plan_hardware'])




                total = 0
                arr = customer_plan_data[0]['customerwithservice']
                arr = arr.replace('"[', '')
                arr = arr.replace(']"', '')
                arr = arr.split(',')
                Arr.append(arr)

                if not arr:
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
                        Total.append(total)

                        # =========================================================================================================================#

                        totalhw = 0
                        arrhwdata = []
                        for ar in arr:
                            hardware = ServicePlanWithHardware.objects.values('id', 'hw_id', 'hw_qty', 'hw_status',
                                                                              'hw_id__hw_title').filter(
                                service_plan_id=ar)
                            for hj in hardware:
                                arrhwdata.append(hj['hw_id'])
                        array = []
                        for h in arrhwdata:
                            vale = Hardware.objects.values('device_buy').filter(pk=h)
                            array.append(vale[0]['device_buy'])

                        for hw in array:
                            totalhw = totalhw + float(hw)
                            Totalhw.append(totalhw)

        # ==================================================================================== Contract List End =============================================================================================#

        # subject = 'Invoice of this month from Egciptv'
        # massege = 'Noise'
        #
        # html_msg = render_to_string('admin/invoice/invoice.html',
        #                             {'CustomerPlanData': str(CustomerPlanData), 'HwDtata': str(HwDtata),
        #                              'Address': address, 'Arr': str(Arr), 'Total': str(Total),
        #                              'Totalhw': str(Totalhw),'fname':cus['first_name'],'lname':cus['last_name']})
        #
        # if contract_list.exists():
        #     send_mail(subject, massege, 'support@25airport.com', [cus['email_address']], fail_silently=False,
        #               html_message=html_msg)
        # else:
        #     pass


sched.start()
