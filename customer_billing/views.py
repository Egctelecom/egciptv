from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View

from adminsidecustomer.models import Customer, CustomerUserMap
from agentpanel.models import Agent
from django.contrib.auth.mixins import LoginRequiredMixin

from crmadmin.models import UserProfile
from customer_billing.models import BillingDetailsCustomer, CreditCard, BankingDetails, PaypalDetails


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
			sales_person = UserProfile.objects.get(id=request.POST['sale_person_id'])
			BillingDetailsCustomer.objects.create(user=customer, salesperson=sales_person,
			                                      contract_type=request.POST['contract_type'],
			                                      billing_day=request.POST['billing_day'],
			                                      payment_mode=request.POST['payment_type'],
			                                      payment_method=request.POST['payment_method'],
			                                      billing_from=request.POST.get('from'), billing_to=request.POST.get('to'))
			messages.success(request, "Data Added.")
		except Exception as e:
			messages.error(request, "Something went wrong - {}".format(e))
		return HttpResponseRedirect(reverse('customer_billing_add'))


class CustomerBillingSetting(View, LoginRequiredMixin):
	login_url = '/admin/'
	
	def post(self, request):
		customer = Customer.objects.get(id=request.POST['customer_id'])
		sales_person = UserProfile.objects.get(user_id=request.POST['sale_person_id'])
		billing = BillingDetailsCustomer.objects.filter(user_id=customer)
		if billing.exists():
			BillingDetailsCustomer.objects.filter(user=customer).update(salesperson_id=sales_person.id,
		                                      contract_type=request.POST['contract_type'],
		                                      billing_day=request.POST['billing_day'],
		                                      # payment_mode=request.POST['payment_type'],
		                                      payment_method=request.POST['payment_method']
		                                      # billing_from=request.POST.get('from'),
		                                      # billing_to=request.POST.get('to')
		                                      )
		else:
			BillingDetailsCustomer.objects.create(user=customer, salesperson_id=sales_person.id,
			                                                            contract_type=request.POST['contract_type'],
			                                                            billing_day=request.POST['billing_day'],
			                                                            # payment_mode=request.POST['payment_type'],
			                                                            payment_method=request.POST['payment_method']
			                                                            # billing_from=request.POST.get('from'),
			                                                            # billing_to=request.POST.get('to')
			                                                            )
		
		# messages.success(request, "Details Updated.")
		return HttpResponseRedirect(reverse('customer_details', kwargs={'id': request.POST['customer_id']}))
		
		

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


class CreditCardAdd(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		# if CreditCard.objects.filter(user__id=id).exists():
		# 	credit_card_obj = CreditCard.objects.get(user__id=id)
		# 	return render(request, 'admin/billing/credit_card_add.html', {'credit_card_obj': credit_card_obj})
		# else:
		customer_obj = Customer.objects.get(id=id)
		year_range = range(2019, 2051)
		return render(request, 'admin/billing/credit_card_add.html', {'customer_obj': customer_obj,
		                                                              'year_range': year_range})
	
	def post(self, request, id):
		# if CreditCard.objects.filter(user__id=id).exists():
		# 	credit_card_obj = CreditCard.objects.get(user__id=id)
		# 	credit_card_obj.card_type = request.POST['card_type']
		# 	credit_card_obj.name = request.POST['card_name']
		# 	credit_card_obj.number = request.POST['card_number']
		# 	credit_card_obj.month = request.POST['month']
		# 	credit_card_obj.year = request.POST['year']
		# 	credit_card_obj.cvv = request.POST['cvv']
		# 	credit_card_obj.primary = request.POST['primary']
		# 	credit_card_obj.save()
		# else:
		try:
			primary = False
			if 'primary' in request.POST and request.POST['primary'] == 'on':
				primary = True
			
			card = CreditCard.objects.create(user=Customer.objects.get(id=id), card_type=request.POST['card_type'],
			                          name=request.POST['card_name'], number=request.POST['card_number'],
			                          month=request.POST['month'],
			                          year=request.POST['year'], cvv=request.POST['cvv'], primary=primary)
			if card.primary == True:
				CreditCard.objects.filter(user=Customer.objects.get(id=id)).exclude(pk=card.id).update(primary=False)
			messages.success(request, "Details Saved.")
		except Exception as e:
			messages.error(request, "Something went wrong - {}".format(e))
		
		customer_obj = Customer.objects.get(id=id)
		year_range = range(2019, 2051)
		return render(request, 'admin/billing/credit_card_add.html', {'customer_obj': customer_obj,
		                                                              'year_range': year_range})


class CreditCardListView(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		queryset = CreditCard.objects.filter(user__id=id)
		
		return render(request, 'admin/billing/credit_card_list.html', {'queryset': queryset, 'id': id})


class CreditCardEditView(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		creditcard_obj = CreditCard.objects.get(id=id)
		year_range = range(2019, 2051)
		return render(request, 'admin/billing/credit_card_edit.html',
		              {'creditcard_obj': creditcard_obj, 'year_range': year_range})
	
	def post(self, request, id):
		credit_card_obj = CreditCard.objects.get(id=id)
		credit_card_obj.card_type = request.POST['card_type']
		credit_card_obj.name = request.POST['card_name']
		credit_card_obj.number = request.POST['card_number']
		credit_card_obj.month = request.POST['month']
		credit_card_obj.year = request.POST['year']
		credit_card_obj.cvv = request.POST['cvv']
		
		if 'primary' in request.POST and request.POST['primary'] == 'on':
			credit_card_obj.primary = True
		else:
			credit_card_obj.primary = False
		credit_card_obj.save()
		
		if credit_card_obj.primary == True:
			CreditCard.objects.filter(user=credit_card_obj.user).exclude(pk=credit_card_obj.id).update(primary=False)
		year_range = range(2019, 2051)
		messages.success(request, "Data Updated")
		return render(request, 'admin/billing/credit_card_edit.html',
		              {'creditcard_obj': credit_card_obj, 'year_range': year_range})


class CreditCardEditDelete(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		credit_card = CreditCard.objects.get(pk=id)
		credit_card.delete()
		return HttpResponseRedirect(reverse('customer_details', kwargs={'id': credit_card.user_id}))


class CreditCardImport(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		return render(request, 'admin/billing/credit_card_import.html',
		              {'user_id': id})
	
	def post(self, request, id):
		account_id = request.POST.get('account_id')
		#-------------------self customer----------------
		# importer_user_id = CustomerUserMap.objects.get(customer_id=id).user_id
		# customer = Customer.objects.get(pk=customer_user_map.customer_id)
		
		other_customer_user = CustomerUserMap.objects.filter(customer__account_id=account_id).values('user', 'customer')
		
		
		customer_card_details = CreditCard.objects.filter(user_id=other_customer_user[0]['customer'], primary=True).values_list('number', flat=True)
		
		
		user_has_same_cards = CreditCard.objects.filter(user=id, number__in=customer_card_details)
		
		customer_has_default_cards = CreditCard.objects.filter(user=id, primary=True).count()
		
		if not user_has_same_cards.exists():
			credit_card = CreditCard.objects.get(number=customer_card_details[0])
			
			if customer_has_default_cards:
				credit_card.primary = False
				
			credit_card.pk = None
			credit_card.user_id = id
			credit_card.save()
			
			messages.add_message(request, messages.SUCCESS, 'Imported Successfully')
		else:
			messages.add_message(request, messages.ERROR, 'Already exists')
		return HttpResponseRedirect(reverse('customer_credit_card_import', kwargs={'id': id}))
		
		
class DirectDeopsitAdd(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		return render(request, 'admin/billing/direct_deposit_add.html',
		              {'user_id': id})
	
	def post(self, request, id):
		BankingDetails.objects.create(user_id=id, branch_id=request.POST.get('branch_id'),
		                              institution_no=request.POST.get('institution_no'), account_no=request.POST.get('account_no'),
		                              account_name=request.POST.get('account_name'), bank_name=request.POST.get('bank_name'))
		
		messages.add_message(request, messages.SUCCESS, 'Details added')
		
		return render(request, 'admin/billing/direct_deposit_add.html',
		              {'user_id': id})


class DirectDeopsitEdit(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		bank_details = BankingDetails.objects.get(id=id)
		return render(request, 'admin/billing/direct_deposit_edit.html',
		              {'bank_details': bank_details})
	
	def post(self, request, id):
		bank_details = BankingDetails.objects.get(id=id)
		bank_details.branch_id = request.POST.get('branch_id')
		bank_details.institution_no = request.POST.get('institution_no')
		bank_details.account_no = request.POST.get('account_no')
		bank_details.account_name = request.POST.get('account_name')
		bank_details.bank_name = request.POST.get('bank_name')
		bank_details.save()
		
		messages.add_message(request, messages.SUCCESS, 'Details updated')
		
		return render(request, 'admin/billing/direct_deposit_edit.html',
		              {'bank_details': bank_details})
	
	
class DirectDeopsitDelete(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		bank_details = BankingDetails.objects.get(pk=id)
		bank_details.delete()
		return HttpResponseRedirect(reverse('customer_details', kwargs={'id': bank_details.user_id}))


class PaypalAddressAdd(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		return render(request, 'admin/billing/paypal_address_add.html',
		              {'user_id': id})
	
	def post(self, request, id):
		PaypalDetails.objects.create(user_id=id, account_id=request.POST.get('account_id'))
		
		messages.add_message(request, messages.SUCCESS, 'Details added')
		
		return render(request, 'admin/billing/paypal_address_add.html',
		              {'user_id': id})


class PaypalAddressEdit(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		paypal_details = PaypalDetails.objects.get(pk=id)
		return render(request, 'admin/billing/paypal_address_edit.html',
		              {'paypal_details': paypal_details})
	
	def post(self, request, id):
		paypal_details = PaypalDetails.objects.get(pk=id)
		paypal_details.account_id = request.POST.get('account_id')
		paypal_details.save()
		
		messages.add_message(request, messages.SUCCESS, 'Details updated')
		
		return render(request, 'admin/billing/paypal_address_edit.html',
		              {'paypal_details': paypal_details})


class PaypalAddressDelete(LoginRequiredMixin, View):
	login_url = '/admin/'
	
	def get(self, request, id):
		paypal_details = PaypalDetails.objects.get(pk=id)
		paypal_details.delete()
		return HttpResponseRedirect(reverse('customer_details', kwargs={'id': paypal_details.user_id}))