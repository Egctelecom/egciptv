# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-13 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminsideserviceprovider', '0010_auto_20191113_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerservicecontract',
            name='type',
            field=models.CharField(choices=[('Renew', 'Renew'), ('New', 'New'), ('Terminate', 'Terminate')], default='New', help_text='Enter Type', max_length=150),
        ),
        migrations.AlterField(
            model_name='customerwithservice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_plans', to='adminsidecustomer.Customer'),
        ),
    ]
