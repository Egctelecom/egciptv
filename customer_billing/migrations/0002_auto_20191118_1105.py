# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-18 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingdetailscustomer',
            name='salesperson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agentpanel.Agent'),
        ),
    ]
