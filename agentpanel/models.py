from django.contrib.auth.models import User
from django.db import models

status = (
        ('Agent', 'Agent'),
)

#----------------------------------------------------------------- Agent add ----------------------------------------------------------

class Agent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(help_text='Enter First Name', max_length=255)
    last_name = models.CharField(help_text='Enter Last Name', max_length=255)
    email_address = models.CharField(help_text='Enter Email Address', max_length=255)
    phone = models.BigIntegerField()
    status = models.CharField(help_text='Enter Status', choices=status, default='Agent', max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id