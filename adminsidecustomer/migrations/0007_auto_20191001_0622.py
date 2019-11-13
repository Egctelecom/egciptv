# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-01 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsidecustomer', '0006_auto_20190803_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingdetailscustomer',
            name='year_pre_payment',
            field=models.CharField(blank=True, help_text='Enter Year Pre Payment', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='company_name_gsr',
            field=models.CharField(blank=True, help_text='Enter GSR', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name_gsr',
            field=models.CharField(blank=True, help_text='Enter GSR', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name_gsr',
            field=models.CharField(blank=True, help_text='Enter GSR', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customerinvoicemap',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', help_text='Enter Status', max_length=150),
        ),
    ]
