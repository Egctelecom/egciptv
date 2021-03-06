# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-08-03 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsideserviceprovider', '0005_auto_20190729_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceproviderplan',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('delete', 'delete')], default='active', help_text='Enter active status', max_length=255),
        ),
        migrations.AlterField(
            model_name='customerservicecontract',
            name='type',
            field=models.CharField(choices=[('Terminate', 'Terminate'), ('New', 'New'), ('Renew', 'Renew')], default='New', help_text='Enter Type', max_length=150),
        ),
    ]
