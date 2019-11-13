from django.db import models
from adminsidecustomer.models import Country,Province,City
from sitefrontendbyadmin.models import MenuCategory
from adminsideserviceprovider.models import ServiceProviderPlan

#==== Customer Apply for service to Admin ====#

class CustomerApplyForService(models.Model):
    id = models.AutoField(primary_key=True)
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    plan = models.ForeignKey(ServiceProviderPlan, on_delete=models.CASCADE)
    first_name = models.CharField(help_text='Enter First Name', max_length=255)
    last_name = models.CharField(help_text='Enter First Name', max_length=255)
    email_address = models.CharField(help_text='Enter Email Address', max_length=255)
    company_name = models.CharField(help_text='Enter Company Name', max_length=255,blank=True,null=True)
    phone = models.BigIntegerField()
    cell_number = models.BigIntegerField()

    call_time = models.CharField(help_text='Enter Call Time', max_length=255,blank=True,null=True)
    installation_time = models.CharField(help_text='Enter Installation Time', max_length=255,blank=True,null=True)
    hear_about_us = models.CharField(help_text='Enter Hear About Us', max_length=255,blank=True,null=True)
    existing_service_provider = models.CharField(help_text='Enter Service Provider', max_length=255,blank=True,null=True)
    service_date_time = models.CharField(help_text='Enter Service Date Time', max_length=255,blank=True,null=True)
    cancellation_date_with_current_provider = models.CharField(help_text='Enter Cancellation Date With Current Provider', max_length=255,blank=True,null=True)
    terms_of_service = models.CharField(help_text='Enter Terms of Service', max_length=255,blank=True,null=True)
    referred_ac_no = models.CharField(help_text='Enter Referred Account No', max_length=255,blank=True,null=True)
    referred_by = models.CharField(help_text='Enter Referred By', max_length=255,blank=True,null=True)
    promo_code = models.CharField(help_text='Enter Promo Code', max_length=255,blank=True,null=True)
    message = models.TextField(help_text='Enter Message', blank=True)

    service_address_1 = models.CharField(help_text='Enter Service Street Number 1', max_length=255)
    service_address_2 = models.CharField(help_text='Enter Service Street Number 2', max_length=255)
    service_apt_suite = models.CharField(help_text='Enter Service Apt./Suite', max_length=255)
    service_city = models.ForeignKey(City, on_delete=models.CASCADE)
    service_province = models.ForeignKey(Province, on_delete=models.CASCADE)
    service_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    service_postcode = models.CharField(help_text='Enter Service Postal Code', max_length=255)

    applied_ip_address = models.CharField(help_text='Enter Ip Address', max_length=255,blank=True)

    previous_invoice = models.FileField(upload_to='static/previous_invoice/',blank=True,null=True)
  
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class CustomerApplyForServiceBilling(models.Model):
	
    id = models.AutoField(primary_key=True)
    customer_apply_for_service = models.ForeignKey(CustomerApplyForService, on_delete=models.CASCADE)
    billing_address_1 = models.CharField(help_text='Enter Billing Street Number 1', max_length=255,blank=True,null=True)
    billing_address_2 = models.CharField(help_text='Enter Billing Street Number 2', max_length=255,blank=True,null=True)
    billing_apt_suite = models.CharField(help_text='Enter Billing Apt./Suite', max_length=255,blank=True,null=True)
    billing_city = models.ForeignKey(City, on_delete=models.CASCADE,blank=True,null=True)
    billing_province = models.ForeignKey(Province, on_delete=models.CASCADE,blank=True,null=True)
    billing_country = models.ForeignKey(Country, on_delete=models.CASCADE,blank=True,null=True)
    billing_postcode = models.CharField(help_text='Enter Billing Postal Code', max_length=255,blank=True,null=True)

    def __str__(self):
	    return self.id
    
    
class Otherdetails(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(help_text='Enter key', max_length=255)
    value = models.TextField(help_text='Enter Value', max_length=255,blank=True)
    address=models.CharField(help_text='Enter Address', max_length=255,blank=True)
    city=models.CharField(help_text='Enter City', max_length=255,blank=True)
    province=models.CharField(help_text='Enter Province', max_length=255,blank=True)
    country=models.CharField(help_text='Enter Country', max_length=255,blank=True)
    zip=models.CharField(help_text='Enter Zip', max_length=255,blank=True)
    fax=models.CharField(help_text='Enter Fax', max_length=255,blank=True)
    phone=models.CharField(help_text='Enter Phone', max_length=255,blank=True)
    email=models.CharField(help_text='Enter Email', max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id
    


    
