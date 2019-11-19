from django.db import models

# Create your models here.
from adminsidecustomer.models import Customer
from agentpanel.models import Agent
from crmadmin.models import UserProfile

PAYMENT_MODE_CHOICES = (
	('ONLINE', 'ONLINE'),
	('OFFLINE', 'OFFLINE')
)

PAYMENT_METHOD_CHOICES = (
	('CASH', 'CASH'),
	('CREDIT CARD', 'CREDIT CARD'),
	# ('INTERNET BANKING', 'INTERNET BANKING'),
	('BANK DEPOSIT', 'BANK DEPOSIT'),
	('PAYPAL', 'PAYPAL')
)

CREDIT_CARD_CHOICES = (
	('VISA', 'VISA'),
	('MASTERCARD', 'MASTERCARD'),
	('AMERICAN EXPRESS', 'AMERICAN EXPRESS')
)


class BillingDetailsCustomer(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(Customer, on_delete=models.CASCADE)
	salesperson = models.ForeignKey(Agent, on_delete=models.CASCADE)
	contract_type = models.CharField(max_length=255)
	billing_day = models.CharField(help_text='Enter Billing Day', max_length=255)
	payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, default='ONLINE', max_length=50)
	payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES, default='CREDIT CARD', max_length=50)
	year_pre_payment = models.CharField(help_text='Enter Year Pre Payment', max_length=255, blank=True, null=True)
	billing_from = models.CharField(help_text='Enter Billing From', max_length=255)
	billing_to = models.CharField(help_text='Enter Billing To', max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.id


class CreditCard(models.Model):
	user = models.ForeignKey(Customer, on_delete=models.CASCADE)
	card_type = models.CharField(max_length=20, choices=CREDIT_CARD_CHOICES)
	name = models.CharField(max_length=255)
	number = models.CharField(max_length=50)
	month = models.IntegerField()
	year = models.IntegerField()
	cvv = models.IntegerField()
	primary = models.BooleanField(default=False)


class PaypalDetails(models.Model):
	user = models.ForeignKey(Customer, on_delete=models.CASCADE)
	account_id = models.CharField(max_length=255)


class BankingDetails(models.Model):
	user = models.ForeignKey(Customer, on_delete=models.CASCADE)
	branch_id = models.CharField(max_length=255)
	institution_no = models.CharField(max_length=255)
	account_no = models.CharField(max_length=255)
	account_name = models.CharField(max_length=255)
	bank_name = models.CharField(max_length=100, blank=True, null=True)
