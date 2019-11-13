from django.db import models
from django.contrib.auth.models import User


payment_status=(
    ('Pending','Pending'),
    ('Complete','Complete'),
    ('Fail','Fail')
)

class CustomerBillingDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_service_contract = models.TextField(help_text='Enter Contract')
    call_cost = models.TextField(help_text='Enter Call Cost')
    previous_balance = models.TextField(help_text='Enter Previous Balance')
    current_balance = models.TextField(help_text='Enter Current Balance')
    due_amount = models.TextField(help_text='Enter Due Amount')
    payment_status = models.CharField(help_text='Enter active payment status', choices=payment_status, default='Pending', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CustomerBillingDetailsWithEdited(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_billing_details = models.ForeignKey(CustomerBillingDetails, on_delete=models.CASCADE)
    reduce_payment = models.TextField(help_text='Enter Reduce Amount')
    paid_payment = models.TextField(help_text='Enter Paid Amount')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
class VoipLongDistanceRate(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(help_text='Enter Country',max_length=255,blank=True,null=True)
    prefix = models.CharField(help_text='Enter Prefix',max_length=255,blank=True,null=True)
    rate = models.CharField(help_text='Enter Rate',max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)