from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from adminsidecustomer.models import Customer
from adminsideserviceprovider.models import CustomerServiceContract

def paypalIPN(request):
    if request.method == 'GET':
        if request.GET['st']== 'Completed':
         contract_id = request.GET['item_number']
         if CustomerServiceContract.objects.filter(pk=contract_id).exists():
             contract = CustomerServiceContract.objects.get(pk=contract_id)
             contract.payment_status = 'Complete'
             contract.save()
             user = CustomerServiceContract.objects.values('user_id').filter(pk=contract_id)
             to_email = Customer.objects.values('email_address', 'first_name', 'last_name').filter(pk=user[0]['user_id'])
             subject = 'Payment Complete of egciptv'
             massege = render_to_string('agent/customer/contract/payment_mail.html',
                                        {'first_name': to_email[0]['first_name'], 'last_name': to_email[0]['last_name'],
                                         'contract_id': contract_id})
             html_msg = render_to_string('agent/customer/contract/payment_mail.html',
                                         {'first_name': to_email[0]['first_name'], 'last_name': to_email[0]['last_name'],
                                          'contract_id': contract_id})
             send_mail(subject, massege, 'support@25airport.com', [to_email[0]['email_address']], fail_silently=False,
                       html_message=html_msg)
             messages.add_message(request, messages.SUCCESS, 'A success mail send to your provided email address')
    return HttpResponseRedirect(reverse('home'))
