from django.db import models
from adminsidecustomer.models import Province, Country, Customer


# ----------------------------------------------------------------- Number Provider ----------------------------------------------------------


class NumberProvinceMap(models.Model):
    id = models.AutoField(primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    did_id = models.CharField(help_text='Enter Did id ', max_length=255)
    npa = models.CharField(help_text='Enter NPA', max_length=255)
    nxx = models.CharField(help_text='Enter NXX', max_length=255)
    xxxx = models.CharField(help_text='Enter XXXX', max_length=255)
    tier = models.CharField(help_text='Enter TIER', max_length=255)
    ratecenters = models.CharField(help_text='Enter Ratecenter', max_length=255)
    number = models.CharField(help_text='Enter number', max_length=255)
    setup_rate = models.CharField(help_text='Enter set up rate', max_length=255)
    monthly_rate = models.CharField(help_text='Enter monthly rate', max_length=255)
    per_minute_rate = models.CharField(help_text='Enter per minitue rate', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class NumberProvinceCustomerMap(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number = models.ForeignKey(NumberProvinceMap, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

class NumberMNPtoCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number = models.BigIntegerField()
    approve_upload_data = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id