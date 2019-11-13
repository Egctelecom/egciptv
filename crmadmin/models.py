from django.contrib.auth.models import User
from django.db import models

# Create your models here.
status = (
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('delete', 'delete')
    )
login_type = (
        ('salesperson', 'Salesperson'),
        ('support', 'Support'),
        ('administrator', 'Administrator')
    )
role_type = (
    ('restricted','Restricted'),
    ('relaxed','Relaxed')
)
call_status = (
    ('if_user_number_source','if_user_number_source'),
    ('if_user_number_destination','if_user_number_destination')
)
#---------------------------------------------------------------- Settings | Services Section------------------------------------------------
class ManageServicesPriceCategory(models.Model):
    id = models.AutoField(primary_key=True)
    service_category_name = models.CharField(help_text='Enter Service Name',max_length=255)
    status = models.CharField(help_text='Enter active status', choices=status, default='active', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class ManageServicePrice(models.Model):
    id = models.AutoField(primary_key=True)
    service_category = models.ForeignKey('ManageServicesPriceCategory', on_delete=models.CASCADE)
    service_name = models.CharField(help_text='Enter Service Name', max_length=255)
    service_price = models.FloatField(help_text='Enter Service Price')
    service_desc = models.TextField(help_text='Enter Service Description',max_length=15000,blank=True)
    service_logo = models.FileField(upload_to='static/service_logo/',blank=True)
    status = models.CharField(help_text='Enter Active Status', choices=status, default='active', max_length=15)
    special_offer = models.CharField(help_text='Enter Special offer',max_length=255,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id



#----------------------------------------------------------------- Settings | Login Section ------------------------------------------------

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_type = models.CharField(help_text='Enter Login Type', choices=login_type, default='salesperson', max_length=50)
    commissions_in_USD = models.FloatField(help_text='Enter Commissions in $')
    commissions_in_percent = models.FloatField(help_text='Enter Commissions in %')
    role = models.CharField(help_text='Enter Role Type', choices=role_type, default='restricted', max_length=50)
    extentions = models.CharField(help_text='Enter Extentions', max_length=255)

    def __str__(self):
        return self.id

#----------------------------------------------------------------- Services ----------------------------------------------------------

class Services(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(help_text='Enter Service Name', max_length=255)
    price = models.FloatField(help_text='Enter Service Price')
    phone_service = models.BooleanField(default=False)
    internet_service = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
    

#----------------------------------------------------------------- User Image  ----------------------------------------------------------


class UserImage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatardata = models.FileField(upload_to='static/avatar/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.avatardata.url
    
#----------------------------------------------------------------- Call Cost  ----------------------------------------------------------


class CallCost(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(help_text='Enter Service Name', max_length=255)
    destination = models.CharField(help_text='Enter Service Name', max_length=255)
    call_cost = models.CharField(help_text='Enter Call Cost', max_length=255)
    start_date = models.CharField(help_text='Enter Start Date', max_length=255)
    end_date = models.CharField(help_text='Enter End Date', max_length=255)
    status = models.CharField(help_text='Enter Status Type', choices=call_status, default='if_user_number_source', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
    
    

    
    
    
