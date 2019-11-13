from django import forms
from egciptvhome.models import CustomerApplyForService,CustomerApplyForServiceBilling

class CustomerApplyForServiceform(forms.ModelForm):
	
	first_name = forms.CharField(help_text='Enter First Name', max_length=255)
	last_name = forms.CharField(help_text='Enter First Name', max_length=255)
	email_address = forms.CharField(help_text='Enter Email Address', max_length=255)
	company_name = forms.CharField(help_text='Enter Company Name', max_length=255,required=False)
	phone = forms.IntegerField()
	cell_number = forms.IntegerField()
	
	call_time = forms.CharField(help_text='Enter Call Time', max_length=255,required=False)
	installation_time = forms.CharField(help_text='Enter Installation Time', max_length=255,required=False)
	hear_about_us = forms.CharField(help_text='Enter Hear About Us', max_length=255,required=False)
	existing_service_provider = forms.CharField(help_text='Enter Service Provider', max_length=255,required=False)
	service_date_time = forms.CharField(help_text='Enter Service Date Time', max_length=255,required=False)
	cancellation_date_with_current_provider = forms.CharField(help_text='Enter Cancellation Date With Current Provider', max_length=255,required=False)
	terms_of_service = forms.CharField(help_text='Enter Terms of Service', max_length=255,required=False)
	referred_ac_no = forms.CharField(help_text='Enter Referred Account No', max_length=255,required=False)
	referred_by = forms.CharField(help_text='Enter Referred By', max_length=255,required=False)
	promo_code = forms.CharField(help_text='Enter Promo Code', max_length=255,required=False)
	message = forms.CharField(max_length=500,widget=forms.Textarea,required=False)
	
	service_address_1 = forms.CharField(help_text='Enter Service Street Number 1', max_length=255)
	service_address_2 = forms.CharField(help_text='Enter Service Street Number 2', max_length=255)
	service_apt_suite = forms.CharField(help_text='Enter Service Apt./Suite', max_length=255)
	service_postcode = forms.CharField(help_text='Enter Service Postal Code', max_length=255)
	
	applied_ip_address = forms.CharField(help_text='Enter Ip Address', max_length=255,required=False)
	
	previous_invoice = forms.FileField(required=False)
	
	class Meta:
		model = CustomerApplyForService
		fields='__all__'


class CustomerApplyForServiceBillingform(forms.ModelForm):
	
	billing_address_1 = forms.CharField(help_text='Enter Billing Street Number 1', max_length=255,required=False)
	billing_address_2 = forms.CharField(help_text='Enter Billing Street Number 2', max_length=255,required=False)
	billing_apt_suite = forms.CharField(help_text='Enter Billing Apt./Suite', max_length=255,required=False)
	billing_postcode = forms.CharField(help_text='Enter Billing Postal Code', max_length=255,required=False)
	
	class Meta:
		model = CustomerApplyForServiceBilling
		fields = '__all__'
