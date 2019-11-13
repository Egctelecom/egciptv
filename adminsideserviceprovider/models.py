from django.db import models
from adminsidecustomer.models import City, Province, Country, Customer
from crmadmin.models import ManageServicePrice, ManageServicesPriceCategory
from django.contrib.auth.models import User

plan_status = (
        ('active', 'Y'),
        ('inactive', 'N'),

    )
type = {
    ('New','New'),
    ('Renew','Renew'),
    ('Terminate','Terminate'),
}
payment_status=(
    ('Pending','Pending'),
    ('Complete','Complete'),
    ('Fail','Fail')
)
hw_status=(
    ('Buy', 'Buy'),
    ('Rental', 'Rental'),
    ('MonthlyRent', 'MonthlyRent')
)

priority = (
        ('low', 'L'),
        ('medium', 'M'),
        ('high', 'H'),

    )
category = (
        ('user', 'U'),
        ('administrator', 'A'),

    )

working_status=(
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Complete', 'Complete')
)
plan_paid_status=(
    ('Monthly', 'Monthly'),
    ('One Time', 'One Time')
)
status = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('delete', 'delete')
    )

class ServiceProvider(models.Model):
    id = models.AutoField(primary_key=True)
    service_provider_name = models.CharField(help_text='Enter Service Provider Name', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class ServiceProviderCityMap(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class ServiceProviderPlan(models.Model):
    id = models.AutoField(primary_key=True)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    manage_service_category = models.ForeignKey(ManageServicesPriceCategory, on_delete=models.CASCADE)
    manage_service = models.ForeignKey(ManageServicePrice, on_delete=models.CASCADE)    
    title = models.CharField(help_text='Enter Service Provider Plan Name', max_length=255)
    retail = models.CharField(help_text='Enter Service Provider Plan Retail Value', max_length=255)
    actual = models.CharField(help_text='Enter Service Provider Plan Actual Value', max_length=255)
    qty = models.CharField(help_text='Enter Service Provider Plan Quantity', max_length=255)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class Hardware(models.Model):
    id = models.AutoField(primary_key=True)
    hw_title = models.CharField(help_text='Enter hardware Name', max_length=255)
    type = models.CharField( max_length=255,blank=True)
    model = models.CharField( max_length=255,blank=True)
    mac = models.CharField( max_length=255,blank=True)
    sn = models.CharField( max_length=255,blank=True)
    ver = models.CharField( max_length=255,blank=True)
    usrn = models.CharField(max_length=255,blank=True)
    passu = models.CharField(max_length=255,blank=True)
    adusr = models.CharField(max_length=255,blank=True)
    adpass = models.CharField( max_length=255,blank=True)
    dslusr = models.CharField(max_length=255,blank=True)
    dslpass = models.CharField(max_length=255,blank=True)
    date_start = models.CharField(max_length=255,blank=True)
    date_end = models.CharField(max_length=255,blank=True)
    still_in_service = models.CharField(max_length=255,blank=True)
    device_buy = models.CharField(help_text='Enter Device Buy', max_length=255,blank=True)
    device_rental = models.CharField(help_text='Enter Device Rental', max_length=255,blank=True)
    montly_rent = models.CharField(help_text='Enter Montly rent', max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ServicePlanWithHardware(models.Model):
    id = models.AutoField(primary_key=True)
    service_plan = models.ForeignKey(ServiceProviderPlan, on_delete=models.CASCADE)
    hw = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    hw_qty = models.CharField(help_text='Enter Service Provider Plan Quantity', max_length=255)
    hw_status = models.CharField(help_text='Enter active hw status', choices=hw_status, default='Buy', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class ManageServicePricedoc(models.Model):
        id = models.AutoField(primary_key=True)
        service_price_provider = models.ForeignKey(ServiceProviderPlan, on_delete=models.CASCADE)
        service_price_doc_name = models.CharField(help_text='Enter Service Price DOC Name', max_length=255, blank=True)
        service_price_doc = models.FileField(upload_to='static/service_price_doc/', blank=True)
        status = models.CharField(help_text='Enter Status', choices=status, default='active', max_length=15)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)


#----------------------------------------------------------------- Service plan with Customer ----------------------------------------------------------

class CustomerWithService(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service_plan = models.ForeignKey(ServiceProviderPlan, on_delete=models.CASCADE)
    service_price_actual = models.FloatField(help_text='Enter Service Price')
    service_price_retail = models.FloatField(help_text='Enter Service Price')
    service_price_qty = models.FloatField(help_text='Enter Service Price')
    plan_status = models.CharField(help_text='Enter active plan status', choices=plan_status, default='y', max_length=150)
    plan_paid_status = models.CharField(help_text='Enter active plan paid status', choices=plan_paid_status, default='Monthly', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

# ----------------------------------------------------------------- Customer Service Contract  ----------------------------------------------------------

class CustomerServiceContract(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customerwithservice = models.TextField(help_text='Enter customer service')
    service_plan_hardware = models.TextField(help_text='Enter service plan h/w')
    type = models.CharField(help_text='Enter Type', choices=type, default='New', max_length=150)
    contract_terms = models.TextField(help_text='Enter contract terms',blank=True)
    payment_status = models.CharField(help_text='Enter active payment status', choices=payment_status, default='Pending', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class TerminateContractDetails(models.Model):
    id = models.AutoField(primary_key=True)
    customercontract = models.ForeignKey(CustomerServiceContract, on_delete=models.CASCADE)
    contract_type = models.CharField(help_text='Enter contract_type', max_length=255)
    contract_date = models.CharField(help_text='Enter contract_date', max_length=255)
    zone = models.CharField(help_text='Enter zone', max_length=255)
    monthly_charge = models.CharField(help_text='Enter monthly_charge', max_length=255)
    outstanding_balance = models.CharField(help_text='Enter outstanding_balance', max_length=255)
    cancellation_date = models.CharField(help_text='Enter cancellation_date', max_length=255)
    cancellation_charge = models.CharField(help_text='Enter cancellation_charge', max_length=255)
    admin_fee = models.CharField(help_text='Enter admin_fee', max_length=255)
    additional_charge = models.CharField(help_text='Enter additional_charge', max_length=255)
    comment = models.TextField(help_text='Enter comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

# ----------------------------------------------------------------- Customer Ticket ----------------------------------------------------------

class TicketsCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category_title = models.CharField(help_text='Enter Category',max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id

class TicketsCategoryWithServiceProvider(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_category = models.ForeignKey(TicketsCategories, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id

class CustomerTicketsCategoriesMap(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ticketCategory = models.ForeignKey(TicketsCategories, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service_plan_hardware = models.ForeignKey(ServicePlanWithHardware, on_delete=models.CASCADE)
    subject = models.TextField(help_text='Enter Subjects', )
    threads = models.TextField(help_text='Enter Threads')
    category = models.CharField(help_text='Enter Category', choices=category, default='U', max_length=150)
    priority = models.CharField(help_text='Enter Status', choices=priority, default='L', max_length=150)
    working_status = models.CharField(help_text='Enter Working Status', choices=working_status, default='Pending', max_length=150)
    updatedby = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    updatedetails = models.TextField(help_text='Enter Update Details',blank=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

#================================================================= Customer contract with mac address of each h/w for each user ====================

class ContractbasedHardwarewithMAC(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hw = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    type = models.CharField( max_length=255,blank=True)
    model = models.CharField( max_length=255,blank=True)
    mac = models.CharField( max_length=255,blank=True)
    sn = models.CharField( max_length=255,blank=True)
    ver = models.CharField( max_length=255,blank=True)
    usrn = models.CharField(max_length=255,blank=True)
    passu = models.CharField(max_length=255,blank=True)
    adusr = models.CharField(max_length=255,blank=True)
    adpass = models.CharField( max_length=255,blank=True)
    dslusr = models.CharField(max_length=255,blank=True)
    dslpass = models.CharField(max_length=255,blank=True)
    date_start = models.CharField(max_length=255,blank=True)
    date_end = models.CharField(max_length=255,blank=True)
    still_in_service = models.CharField(max_length=255,blank=True)
    device_buy = models.CharField(help_text='Enter Device Buy', max_length=255,blank=True)
    device_rental = models.CharField(help_text='Enter Device Rental', max_length=255,blank=True)
    montly_rent = models.CharField(help_text='Enter Montly rent', max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
 #============================================================= Special offer of service plan =======================================
 
 



