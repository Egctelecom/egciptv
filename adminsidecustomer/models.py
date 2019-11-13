from django.db import models
from django.contrib.auth.models import User
from crmadmin.models import Services
from crmadmin.models import UserProfile
zone = (
        ('commercial', 'commercial'),
        ('residential', 'residential'),

    )

display_name = (
            ('user_name', 'user_name'),
            ('company_name', 'company_name'),
            )

prefferd_language = (
            ('english', 'english'),
            ('french', 'french'),
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

amount_type = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
        ('Late Payemt Free Credit', 'Late Payemt Free Credit'),
        ('Late Payemt Free Debit', 'Late Payemt Free Debit'),

    )

end_term = {
        ('True', 'T'),
        ('False', 'F'),
}

invoice_status = {
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
}
tax_status = {
        ('True', 'True'),
        ('False', 'False'),
}
account_status = {
        ('True', 'True'),
        ('False', 'False'),
}

#----------------------------------------------------------------- Country ----------------------------------------------------------

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_name = models.CharField(help_text='Enter Country Name', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


#----------------------------------------------------------------- Province ----------------------------------------------------------

class Province(models.Model):
    id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    province_name = models.CharField(help_text='Enter Province Name', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


# ----------------------------------------------------------------- City ----------------------------------------------------------

class City(models.Model):
    id = models.AutoField(primary_key=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    city_name = models.CharField(help_text='Enter City Name', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
#----------------------------------------------------------------- Customer ----------------------------------------------------------

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.CharField(help_text='Enter Account Id', max_length=255)
    status = models.CharField(help_text='Enter Status', max_length=255)
    first_name = models.CharField(help_text='Enter First Name', max_length=255)
    first_name_gsr = models.CharField(help_text='Enter GSR', max_length=255,blank=True,null=True)
    last_name = models.CharField(help_text='Enter First Name', max_length=255)
    last_name_gsr = models.CharField(help_text='Enter GSR', max_length=255,blank=True,null=True)
    company_name = models.CharField(help_text='Enter Company Name', max_length=255,blank=True,null=True)
    company_name_gsr = models.CharField(help_text='Enter GSR', max_length=255,blank=True,null=True)
    email_address = models.CharField(help_text='Enter Email Address', max_length=255)
    phone = models.BigIntegerField()
    other_phone = models.BigIntegerField()
    portal_password = models.CharField(help_text='Enter Portal Password', max_length=255)
    dob = models.CharField(help_text='Enter Date Of Birth', max_length=255)
    display_name = models.CharField(help_text='Enter active status', choices=display_name, default='user_name', max_length=150)
    prefferd_language = models.CharField(help_text='Enter active status', choices=prefferd_language, default='english', max_length=150)
    zone = models.CharField(help_text='Enter active zone', choices=zone, default='commercial', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class CustomerUserMap(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#----------------------------------------------------------------- Customer Account Address ----------------------------------------------------------

class AccountAddressCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_1 = models.CharField(help_text='Enter Address 1', max_length=255)
    address_2 = models.CharField(help_text='Enter Address 2', max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    postal = models.IntegerField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
#----------------------------------------------------------------- Customer Billing Address ----------------------------------------------------------

class BillingAddressCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    billing_address_1 = models.CharField(help_text='Enter Billing Address 1', max_length=255)
    billing_address_2 = models.CharField(help_text='Enter Billing Address 2', max_length=255)
    billing_city = models.ForeignKey(City, on_delete=models.CASCADE)
    billing_province = models.ForeignKey(Province, on_delete=models.CASCADE)
    billing_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    postal = models.IntegerField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


#----------------------------------------------------------------- Customer Billing Details ----------------------------------------------------------

class BillingDetailsCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    contract_type = models.CharField(help_text='Enter Contract Type', max_length=255)
    billing_day = models.CharField(help_text='Enter Billing Day', max_length=255)
    payment_mode = models.CharField(help_text='Enter Payment Mode', max_length=255)
    payment_method = models.CharField(help_text='Enter Payment Method', max_length=255)
    year_pre_payment = models.CharField(help_text='Enter Year Pre Payment', max_length=255,blank=True,null=True)
    billing_from = models.CharField(help_text='Enter Billing From', max_length=255)
    billing_to = models.CharField(help_text='Enter Billing To', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

#----------------------------------------------------------------- Customer Documents Upload ----------------------------------------------------------

class CutomerAttachmentMap(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    file_name = models.TextField(help_text='Enter File Name ')
    filedata = models.FileField(upload_to='static/attachments/')
    file_type = models.TextField(help_text='Enter File Type ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filedata.url



# ----------------------------------------------------------------- Customer Pending Invoice Details  ----------------------------------------------------------

class CustomerInvoiceMap(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    details = models.TextField(help_text='Enter Detils')
    invoice_month = models.TextField(help_text='Enter Invoive Month')
    amount_type = models.CharField(help_text='Enter Category', choices=amount_type, default='Debit', max_length=150)
    end_term = models.CharField(help_text='Enter End Term', choices=end_term, default='T', max_length=150)
    status = models.CharField(help_text='Enter Status', choices=invoice_status, default='Pending', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


# ----------------------------------------------------------------- Customer Pending Invoice Details  ----------------------------------------------------------

class CustomerComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    touser = models.ForeignKey(User,related_name="touser", on_delete=models.CASCADE)
    comment = models.TextField(help_text='Enter Comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

# ----------------------------------------------------------------- Sales Tax ----------------------------------------------------------

class Sales_tax(models.Model):
        id = models.AutoField(primary_key=True)
        province = models.ForeignKey(Province, on_delete=models.CASCADE)
        tax_name = models.CharField(help_text='Enter Province Name', max_length=255)
        abbreviation = models.CharField(help_text='Enter Province Name', max_length=255)
        description = models.TextField(help_text='Enter Province Name')
        tax_number = models.BigIntegerField()
        is_tax_number_show = models.CharField(help_text='Enter Tax Number Show', choices=tax_status, default='False', max_length=150)
        is_fedral_tax = models.CharField(help_text='Enter Fedral Tax', choices=tax_status, default='False', max_length=150)
        is_provisional_tax = models.CharField(help_text='Enter Provisional Tax', choices=tax_status, default='False', max_length=150)
        tax_rate = models.FloatField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.id

# ----------------------------------------------------------------- Customer Status ----------------------------------------------------------

class CustomerAccountStatus(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contract_sent = models.CharField(help_text='Enter Contract Sent', choices=account_status, default='False', max_length=150)
    contract_accepted = models.CharField(help_text='Enter Contract Accepted', choices=account_status, default='False', max_length=150)
    first_payment_done = models.CharField(help_text='Enter First Payment Done', choices=account_status, default='False', max_length=150)
    req_has_been_sent = models.CharField(help_text='Enter Req has been sent', choices=account_status, default='False', max_length=150)
    devices_shipped = models.CharField(help_text='Enter Devices Shipped ', choices=account_status, default='False', max_length=150)
    devices_received = models.CharField(help_text='Enter Devices Received ', choices=account_status, default='False', max_length=150)
    installation_date = models.CharField(help_text='Enter Installation Date', choices=account_status, default='False', max_length=150)
    installation_done = models.CharField(help_text='Enter Installation Done', choices=account_status, default='False', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

