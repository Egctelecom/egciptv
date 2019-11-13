from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from adminsidecustomer.models import Country,Province,City
from sitefrontendbyadmin.models import MenuCategory
from egciptvhome.forms import CustomerApplyForServiceform,CustomerApplyForServiceBillingform
from egciptvhome.models import CustomerApplyForServiceBilling
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage
from sitefrontendbyadmin.models import SpecialOffers,SpecialoffersUnderCategory

def apply_for_registration(request,menu_id,service_id,type):
	
	if request.method == 'GET':
		
		if type == 'normal':
			country = Country.objects.values('country_name','id').filter(country_name=request.session['country'])
			province = Province.objects.values('country_id_id','province_name','id')
			city = City.objects.values('province_id_id','province_id_id__country_id_id','city_name','id')
			
			category = MenuCategory.objects.values('service_category_id',
			                                       'service_category_id__service_category_name',
			                                       'service_parent_category_id',
			                                       'service_parent_category_id__service_parent_category_name',
			                                       'service_sub_parent_category_name_id',
			                                       'service_sub_parent_category_name_id__service_sub_parent_category_name',
			                                       'id').filter(pk=menu_id)
			
			return render(request, 'egciptv/registration/index.html',{'country': country, 'province': province,'city':city,'category':category,'menu_id':menu_id,'type':type,'service_id':service_id})


	
	elif request.method == 'POST':
		if User.objects.filter(email=request.POST['email_address']).exists():
			
			messages.add_message(request, messages.SUCCESS,
			                     'Email Aleady Exits')
			return HttpResponseRedirect(
				reverse('apply_for_registration', kwargs={'menu_id': menu_id, 'service_id': service_id,'type':type}))
		
		else:
		
			form = CustomerApplyForServiceform(request.POST,request.FILES)
			if form.is_valid():
				billing = form.save()
				billing_address_1 = request.POST['billing_address_1']
				billing_address_2 = request.POST['billing_address_2']
				billing_apt_suite = request.POST['billing_apt_suite']
				billing_city = request.POST['billing_city']
				billing_province = request.POST['billing_province']
				billing_country = request.POST['billing_country']
				billing_postcode = request.POST['billing_postcode']
				
				CustomerApplyForServiceBilling.objects.create(customer_apply_for_service_id=billing.id,
				                                              billing_address_1=billing_address_1,
				                                              billing_address_2=billing_address_2,
				                                              billing_apt_suite=billing_apt_suite,
				                                              billing_city_id=billing_city,
				                                              billing_province_id=billing_province,
				                                              billing_country_id=billing_country,
				                                              billing_postcode=billing_postcode)
				
				subject = 'Congratulation ! You are apply for new service'
				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				to_email = request.POST['email_address']
				
				massege = render_to_string('egciptv/mail/confirmmail.html',{'first_name': first_name, 'last_name': last_name,'menu_id': menu_id,'service_id':service_id})
				
				html_msg = render_to_string('egciptv/mail/confirmmail.html',{'first_name': first_name, 'last_name': last_name,'menu_id': menu_id,'service_id':service_id})
				
				send_mail(subject, massege, 'support@25airport.com', [to_email], fail_silently=False,html_message=html_msg)
				
				subject2 = 'A new User Apply'
				to_email2 = User.objects.values('email', 'username').filter(is_superuser='True')
				
				massege = render_to_string('egciptv/mail/confirmmail.html',
				                           {'first_name': first_name, 'last_name': last_name, 'menu_id': menu_id,
				                            'service_id': service_id})
				
				html_msg = render_to_string('egciptv/mail/confirmmail.html',
				                            {'first_name': first_name, 'last_name': last_name, 'menu_id': menu_id,
				                             'service_id': service_id})
				
				send_mail(subject2, massege, 'support@25airport.com', [to_email2[0]['email']], fail_silently=False, html_message=html_msg)
				
				
				
				
				messages.add_message(request, messages.SUCCESS, 'Apply For Service Send to Egciptv Successfully.A Reporting Mail Send to Admin.Please Wait for Confirmation.')
				return HttpResponseRedirect(reverse('apply_for_registration', kwargs={'menu_id': menu_id,'service_id':service_id,'type':type}))
			else:
				messages.add_message(request, messages.ERROR, form.errors)
				return HttpResponseRedirect(reverse('apply_for_registration', kwargs={'menu_id': menu_id,'service_id':service_id,'type':type}))




def apply_for_registrations_special_offers(request,id):
	if request.method=='GET':
		country = Country.objects.values('country_name', 'id').filter(country_name=request.session['country'])
		province = Province.objects.values('country_id_id', 'province_name', 'id')
		city = City.objects.values('province_id_id', 'province_id_id__country_id_id', 'city_name', 'id')
		
		sp = SpecialoffersUnderCategory.objects.values('id',
		                                               'special_offers_parent_category_id',
		                                               'special_offers_parent_category_id__special_offers_parent_category_name',
		                                               'special_offers_parent_category_id__desc',
		                                               'special_offers_sub_parent_category_id',
		                                               'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
		                                               'special_offers_sub_parent_category_id__desc',
		                                               'special_offers_combo_name',
		                                               'special_offers_type_name',
		                                               'province_id',
		                                               'province_id__province_name',
		                                               'city_id',
		                                               'city_id__city_name',
		                                               'telecom_name',
		                                               'telecom_logo',
		                                               'status',
		                                               'special_offers_id',
		                                               'special_offers_id__actual_price',
		                                               'special_offers_id__offers_price',
		                                               'special_offers_id__details',
		                                               ).filter(special_offers_id=id)
		
		return render(request, 'egciptv/registration/special_offer_index.html',
		              {'country': country, 'province': province, 'city': city,'id':id,'sp':sp})
		