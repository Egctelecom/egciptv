from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View

from adminsidecustomer.models import Customer
from agentpanel.models import Agent
from django.contrib.auth.mixins import LoginRequiredMixin
from customer_billing.models import BillingDetailsCustomer, CreditCard


class CustomerDetails(View, LoginRequiredMixin):
	login_url = '/admin/'
	
	def get(self, request):
		queryset = BillingDetailsCustomer.objects.all()
		return render(request, 'admin/billing/list.html', {'queryset': queryset})


class CustomerBillingAdd(View, LoginRequiredMixin):
	login_url = '/admin/'
	
	def get(self, request):
		customers = Customer.objects.all()
		sales_list = Agent.objects.all()
		return render(request, 'admin/billing/add.html', {'customers': customers, 'sales_list': sales_list})
	
	def post(self, request):
		try:
			customer = Customer.objects.get(id=request.POST['customer_id'])
			sales_person = Agent.objects.get(id=request.POST['sale_person_id'])
			BillingDetailsCustomer.objects.create(user=customer, salesperson=sales_person,
			                                      contract_type=request.POST['contract_type'],
			                                      billing_day=request.POST['billing_day'],
			                                      payment_mode=request.POST['payment_type'],
			                                      payment_method=request.POST['payment_method'],
			                                      billing_from=request.POST['from'], billing_to=request.POST['to'])
			messages.success(request, "Data Added.")
		except Exception as e:
			messages.error(request, "Something went wrong - {}".format(e))
		return HttpResponseRedirect(reverse('customer_billing_add'))


class CustomerBillingEdit(View, LoginRequiredMixin):
	login_url = '/admin/'
	
	def get(self, request, id):
		customers = Customer.objects.all()
		sales_list = Agent.objects.all()
		details = BillingDetailsCustomer.objects.get(id=id)
		return render(request, 'admin/billing/edit.html',
		              {'customers': customers, 'sales_list': sales_list, 'details': details})
	
	def post(self, request, id):
		try:
			customer = Customer.objects.get(id=request.POST['customer_id'])
			sales_person = Agent.objects.get(id=request.POST['sale_person_id'])
			billing_obj = BillingDetailsCustomer.objects.get(id=id)
			billing_obj.user = customer
			billing_obj.salesperson = sales_person
			billing_obj.contract_type = request.POST['contract_type']
			billing_obj.billing_day = request.POST['billing_day']
			billing_obj.payment_mode = request.POST['payment_type']
			billing_obj.payment_method = request.POST['payment_method']
			billing_obj.billing_from = request.POST['from']
			billing_obj.billing_to = request.POST['to']
			billing_obj.save()
			messages.success(request, "Data Updated")
		except Exception as e:
			messages.error(request, "Something went wrong. - {}".format(e))
		return HttpResponseRedirect(reverse('customer_billing_edit', kwargs={'id': id}))
	
	
class CreditCardView(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		if CreditCard.objects.filter(user__id=id).exists():
			credit_card_obj = CreditCard.objects.get(user__id=id)
			return render(request, 'admin/billing/credit_card.html', {'credit_card_obj': credit_card_obj})
		else:
			return render(request, 'admin/billing/credit_card_add.html')
		
	def post(self, request, id):
		if CreditCard.objects.filter(user__id=id).exists():
			credit_card_obj = CreditCard.objects.get(user__id=id)
			credit_card_obj.card_type = request.POST['card_type']
			credit_card_obj.name = request.POST['card_name']
			credit_card_obj.number = request.POST['card_number']
			credit_card_obj.month = request.POST['month']
			credit_card_obj.year = request.POST['year']
			credit_card_obj.cvv = request.POST['cvv']
			credit_card_obj.primary = request.POST['primary']
			credit_card_obj.save()
		else:
			CreditCard.objects.create(user=Customer.objects.get(id=id), card_type=request.POST['card_type'],
			name=request.POST['card_name'], number=request.POST['card_number'], month=request.POST['month'],
			year=request.POST['year'], cvv=request.POST['cvv'], primary=request.POST['primary'])
			
		messages.success(request, "Details Saved.")
		return render(request, 'admin/billing/credit_card_add.html')


class CreditCardListView(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		queryset = CreditCard.objects.filter(user__id=id)
		return render(request, 'admin/billing/credit_card_list.html', {'queryset': queryset})