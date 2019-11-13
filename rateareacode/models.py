from django.contrib.auth.models import User
from django.db import models
from adminsidecustomer.models import UserProfile,Province,Country
status = (
        ('True', 'True'),
        ('False', 'False'),
)

#----------------------------------------------------------------- Rate with area code ----------------------------------------------------------

class Ratewithareacode(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    province = models.ForeignKey(Province,on_delete=models.CASCADE,blank=True)
    area_code = models.CharField(help_text='Enter area code', max_length=255)
    rate = models.FloatField(help_text='Enter rate', max_length=255)
    status = models.CharField(help_text='Enter Status', choices=status, default='True', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

