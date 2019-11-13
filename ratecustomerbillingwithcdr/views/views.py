from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test




import requests
from adminnumberprovider.models import NumberMNPtoCustomer
from adminsidecustomer.models import Customer,CustomerUserMap
from adminnumberprovider.templatetags.check_number_functions import is_number_plus,check_number,check_number2,is_rate_code_chart_plus,cost,plus_cost
from adminsideserviceprovider.models import CustomerServiceContract
from ratecustomerbillingwithcdr.models import CustomerBillingDetails,CustomerBillingDetailsWithEdited
from crmadmin.models import CallCost
from datetime import datetime
import json
from adminsideserviceprovider.models import CustomerServiceContract, CustomerWithService, TerminateContractDetails,ServiceProviderPlan, ServicePlanWithHardware, Hardware,ContractbasedHardwarewithMAC
from adminsidecustomer.models import Customer, AccountAddressCustomer
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User


def my_check(user):
	return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def index(request,id):
	if request.method == 'GET':
		user = CustomerUserMap.objects.filter(customer_id=id).first()
		customer = Customer.objects.filter(pk=id).first()
		if user:
			bill = CustomerBillingDetails.objects.values('id','user_id','user_id__first_name','customer_service_contract','call_cost','payment_status','created_at').filter(user_id=user.user_id)
			return render(request, 'admin/rate_customer_billing_cdr/index.html',{'bill':bill,'id':id,'name':customer.first_name})
		
	
	
	
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def test(request):
	if request.method == 'GET':

		#pass

		customer_list = Customer.objects.values('id', 'first_name', 'last_name', 'email_address')

		contract = []
		callcost = []
		CustomerPlanData = []
		HwDtata = []
		Arr = []
		Address = []
		Total = []
		Totalhw = []
		Previous_balance=[]
		Current_balance=[]
		Due_amt=[]
		# for cus in customer_list:

		address = AccountAddressCustomer.objects.values(
			'id',
			'user_id',
			'address_1',
			'address_2',
			'city__city_name',
			'province__province_name',
			'country__country_name'
		).filter(user_id=16)


		contract_list = CustomerServiceContract.objects.values('id', 'customerwithservice', 'type',
		                                                       'service_plan_hardware').filter(user_id=16,payment_status='Pending',type='New')
		sum_of_amount = 0
		for cl in contract_list:
			arr = cl['customerwithservice']
			arr = arr.replace('"[', '')
			arr = arr.replace(']"', '')
			arr = arr.split(',')
			sum_of_amount=0
			for ar in arr:
				service_plan = CustomerWithService.objects.values(
					'id',
					'service_plan_id__title',
					'service_price_actual',
					'service_price_retail',
					'service_price_qty',
					'plan_status'
				).filter(service_plan_id=ar,plan_paid_status='Monthly',plan_status='y')
				if service_plan:
					ml = service_plan[0]['service_price_actual'] * service_plan[0]['service_price_qty']
					sum_of_amount = sum_of_amount + ml
					contract.append(cl['id'])
		Previous_balance.append(sum_of_amount)

		user = CustomerUserMap.objects.filter(customer_id=16).first()
		if user:
			call_cost_list = CallCost.objects.values('id', 'call_cost').filter(user_id=user.user_id,
			                                                                   start_date__gte='01-01-2018',
			                                                                   start_date__lte='10-01-2018')
			cost_amt=0
			for cl in call_cost_list:
				cost_amt = cost_amt + float(cl['call_cost'])
				callcost.append(cl['id'])
			Current_balance.append(cost_amt)

			due_amt=0
			i=0
			for bal in Previous_balance:
				due_amt =  bal + Current_balance[i]
				i = i+1
			Due_amt.append(due_amt)




		if user:

			billing_details = CustomerBillingDetails.objects.create(user_id=user.user_id,
			                                                        customer_service_contract=json.dumps(contract),
			                                                        call_cost=json.dumps(callcost),
			                                                        previous_balance=json.dumps(Previous_balance),
			                                                        current_balance=json.dumps(Current_balance),
			                                                        due_amount= json.dumps(Due_amt),
			                                                        payment_status='Pending')



		#================================================================================= Contract List================================================================================================#

			customerServiceContract = json.loads(billing_details.customer_service_contract)


			for csc in customerServiceContract:
				id=csc
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
							                                                  'hw_id__hw_title').filter(service_plan_id=ar)
							for hj in hardware:
								arrhwdata.append(hj['hw_id'])
						array = []
						for h in arrhwdata:
							vale = Hardware.objects.values('device_buy').filter(pk=h)
							array.append(vale[0]['device_buy'])

						for hw in array:
							totalhw = totalhw + float(hw)
							Totalhw.append(totalhw)

			billing_details_update = CustomerBillingDetails.objects.get(pk=billing_details.id)
			billing_details_update.previous_balance = json.dumps(Total)



		#==================================================================================== Contract List End =============================================================================================#



			# subject = 'Invoice of this month from Egciptv'
			# massege = 'Noise'
			#
			# html_msg = render_to_string('admin/invoice/invoice.html',{'CustomerPlanData':str(CustomerPlanData),'HwDtata':str(HwDtata),'Address':address,'Arr':str(Arr),'Total':str(Total),'Totalhw':str(Totalhw),'fname':cus['first_name'],'lname':cus['last_name']})
			#
			# if contract_list.exists():
			# 	send_mail(subject, massege, 'support@25airport.com', [cus['email_address']], fail_silently=False,
		    #     		         html_message=html_msg)
			# else:
			# 	pass


	return HttpResponseRedirect(reverse('dashboard'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def billing_details(request,id):
	if request.method == 'GET':
		
			billing_details = CustomerBillingDetails.objects.values('customer_service_contract',
			                                                        'call_cost',
			                                                        'previous_balance',
			                                                        'current_balance',
			                                                        'due_amount',
			                                                        'payment_status',
			                                                        'user_id',
			                                                        'created_at'
			                                                        ).filter(pk=id)
		
			if billing_details:
				customer_data = CustomerUserMap.objects.values('id',
				                                               'customer_id',
				                                               'customer_id__last_name',
				                                               'customer_id__first_name',
				                                               'customer_id__account_id',
				                                               'customer_id__created_at',
				                                               'customer_id__email_address'
				                                               ).filter(user_id=billing_details[0]['user_id'])
				if customer_data:
					customer_address = AccountAddressCustomer.objects.values(
						'id',
						'user_id',
						'address_1',
						'address_2',
						'city__city_name',
						'province__province_name',
						'country__country_name'
					).filter(user_id=customer_data[0]['customer_id'])
					
					

					return render(request,'admin/invoice/invoice.html',{'billing_details': billing_details,
					                                                    'customer_first_name':customer_data[0]['customer_id__first_name'],
					                                                    'customer_last_name':customer_data[0]['customer_id__last_name'],
					                                                    'customer_email':customer_data[0]['customer_id__email_address'],
					                                                    'customer_account_id':customer_data[0]['customer_id__account_id'],
					                                                    'billing_created_at':billing_details[0]['created_at'],
					                                                    'customer_address':customer_address})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def billing_details_edited(request,id):
	if request.method == 'GET':
		
		billing_details = CustomerBillingDetails.objects.values('customer_service_contract',
		                                                        'call_cost',
		                                                        'previous_balance',
		                                                        'current_balance',
		                                                        'due_amount',
		                                                        'payment_status',
		                                                        'user_id',
		                                                        'created_at'
		                                                        ).filter(pk=id)
		
		rate_data = CustomerBillingDetailsWithEdited.objects.values('customer_billing_details_id',
		                                                'customer_billing_details_id__customer_service_contract'
		                                                'customer_billing_details_id__call_cost'
		                                                'customer_billing_details_id__previous_balance',
		                                                'customer_billing_details_id__current_balance',
		                                                'customer_billing_details_id__due_amount',
		                                                'customer_billing_details_id__payment_status',
		                                                'reduce_payment',
		                                                'paid_payment').filter(customer_billing_details_id=id)
		
		if billing_details:
			customer_data = CustomerUserMap.objects.values('id',
			                                               'customer_id',
			                                               'customer_id__last_name',
			                                               'customer_id__first_name',
			                                               'customer_id__account_id',
			                                               'customer_id__created_at',
			                                               'customer_id__email_address'
			                                               ).filter(user_id=billing_details[0]['user_id'])
			if customer_data:
				customer_address = AccountAddressCustomer.objects.values(
					'id',
					'user_id',
					'address_1',
					'address_2',
					'city__city_name',
					'province__province_name',
					'country__country_name'
				).filter(user_id=customer_data[0]['customer_id'])
				
				
				return render(request, 'admin/invoice/new_edited_invoice.html', {'billing_details': billing_details,
				                                                      'customer_first_name': customer_data[0][
					                                                      'customer_id__first_name'],
				                                                      'customer_last_name': customer_data[0][
					                                                      'customer_id__last_name'],
				                                                      'customer_email': customer_data[0][
					                                                      'customer_id__email_address'],
				                                                      'customer_account_id': customer_data[0][
					                                                      'customer_id__account_id'],
				                                                      'billing_created_at': billing_details[0][
					                                                      'created_at'],
				                                                      'customer_address': customer_address,
				                                                      'rate_data': rate_data
				                                                      })
			
			
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def billing_edit(request, id):
	if request.method =='GET':
		billing_details = CustomerBillingDetails.objects.values('customer_service_contract',
		                                                        'call_cost',
		                                                        'previous_balance',
		                                                        'current_balance',
		                                                        'due_amount',
		                                                        'payment_status',
		                                                        'user_id',
		                                                        'created_at'
		                                                        ).filter(pk=id)
		
		if billing_details:
			customer_data = CustomerUserMap.objects.values('id',
			                                               'customer_id',
			                                               'customer_id__last_name',
			                                               'customer_id__first_name',
			                                               'customer_id__account_id',
			                                               'customer_id__created_at',
			                                               'customer_id__email_address'
			                                               ).filter(user_id=billing_details[0]['user_id'])
			if customer_data:
				customer_address = AccountAddressCustomer.objects.values(
					'id',
					'user_id',
					'address_1',
					'address_2',
					'city__city_name',
					'province__province_name',
					'country__country_name'
				).filter(user_id=customer_data[0]['customer_id'])
				
				return render(request, 'admin/invoice/edit_invoice.html', {'id':id,
																	  'billing_details': billing_details,
				                                                      'customer_first_name': customer_data[0][
					                                                      'customer_id__first_name'],
				                                                      'customer_last_name': customer_data[0][
					                                                      'customer_id__last_name'],
				                                                      'customer_email': customer_data[0][
					                                                      'customer_id__email_address'],
				                                                      'customer_account_id': customer_data[0][
					                                                      'customer_id__account_id'],
				                                                      'billing_created_at': billing_details[0][
					                                                      'created_at'],
				                                                      'customer_address': customer_address})
	
	
	
	
def rate_customer_billing_cdr_billing_edit_data(request):
	if request.is_ajax():
		totalAmnt = float(request.POST['totalAmnt'])
		previousAmnt = float(request.POST['previousAmnt'])
		id = request.POST['id']
		billing = CustomerBillingDetails.objects.values('id',
		                                                'customer_service_contract',
		                                                'call_cost',
		                                                'previous_balance',
		                                                'current_balance',
		                                                'due_amount',
		                                                'payment_status',
		                                                'user_id',
		                                                'created_at'
		                                                ).filter(pk=id)
		
		
		print(billing)
		if previousAmnt > totalAmnt:
			
			current_amount = previousAmnt - totalAmnt
			
			CustomerBillingDetailsWithEdited.objects.create(user_id=billing[0]['user_id'],
			                                                customer_billing_details_id=billing[0]['id'],
			                                                reduce_payment=current_amount,
			                                                paid_payment=totalAmnt
			                                                )
			
			response_data = {}
			response_data['amount'] = totalAmnt
			response_data['success'] = 'true'
			return JsonResponse(response_data, safe=False)
		
		else:
			
			response_data = {}
			response_data['amount'] = totalAmnt
			response_data['success'] = 'true'
			return JsonResponse(response_data, safe=False)
		
	
	
	
	
	
	