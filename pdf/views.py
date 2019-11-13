import datetime
import json
import random

from django.http import HttpResponse
from django.views.generic import View

from adminsidecustomer.models import AccountAddressCustomer
from adminsideserviceprovider.models import ServicePlanWithHardware, CustomerWithService, CustomerServiceContract, \
    Hardware
from pdf.utils import render_to_pdf,render_to_pdf_french # created in step 4


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        id =  request.session['contract_id']
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

        # =========================================================================================================================#

        totalhw = 0
        arrhwdata = []
        for ar in arr:
            hardware = ServicePlanWithHardware.objects.values('id', 'hw_id', 'hw_qty', 'hw_status',
                                                              'hw_id__hw_title').filter(service_plan_id=ar)
            for hj in hardware:
                arrhwdata.append(hj['hw_id'])
        print(arrhwdata)
        array = []
        for h in arrhwdata:
            vale = Hardware.objects.values('device_buy').filter(pk=h)
            array.append(vale[0]['device_buy'])

        for hw in array:
            totalhw = totalhw + float(hw)

        pdf = render_to_pdf('admin/customer/contract/mail/contract_attch.html',
                            {
                                'id': id,
                                'customer_plan_data': customer_plan_data,
                                'hwDtata': json.loads(customer_plan_data[0]['service_plan_hardware']),
                                'contractData': arr,
                                'customerwithservicetotal': total,
                                'hw_total': totalhw,
                                'random_no': n,
                                'address': address
                             })
        return HttpResponse(pdf, content_type='application/pdf')


class GeneratePdffrench(View):
    def get(self, request, *args, **kwargs):
        id =  request.session['contract_id']
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

        # =========================================================================================================================#

        totalhw = 0
        arrhwdata = []
        for ar in arr:
            hardware = ServicePlanWithHardware.objects.values('id', 'hw_id', 'hw_qty', 'hw_status',
                                                              'hw_id__hw_title').filter(service_plan_id=ar)
            for hj in hardware:
                arrhwdata.append(hj['hw_id'])
        print(arrhwdata)
        array = []
        for h in arrhwdata:
            vale = Hardware.objects.values('device_buy').filter(pk=h)
            array.append(vale[0]['device_buy'])

        for hw in array:
            totalhw = totalhw + float(hw)

        pdf = render_to_pdf_french('admin/customer/contract/mail/contract_attch_french.html',
                            {
                                'id': id,
                                'customer_plan_data': customer_plan_data,
                                'hwDtata': json.loads(customer_plan_data[0]['service_plan_hardware']),
                                'contractData': arr,
                                'customerwithservicetotal': total,
                                'hw_total': totalhw,
                                'random_no': n,
                                'address': address
                             })

        return HttpResponse(pdf, content_type='application/pdf')