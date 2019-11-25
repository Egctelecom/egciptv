# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-18 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_billing', '0002_auto_20191118_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingdetailscustomer',
            name='contract_type',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='billingdetailscustomer',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'CASH'), ('CREDIT CARD', 'CREDIT CARD'), ('INTERNET BANKING', 'INTERNET BANKING'), ('BANK DEPOSIT', 'BANK DEPOSIT'), ('PAYPAL', 'PAYPAL')], default='CREDIT CARD', max_length=50),
        ),
        migrations.AlterField(
            model_name='billingdetailscustomer',
            name='payment_mode',
            field=models.CharField(choices=[('ONLINE', 'ONLINE'), ('OFFLINE', 'OFFLINE')], default='ONLINE', max_length=50),
        ),
    ]
