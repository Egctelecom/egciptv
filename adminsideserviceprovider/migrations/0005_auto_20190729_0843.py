# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-29 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsideserviceprovider', '0004_auto_20190717_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerservicecontract',
            name='type',
            field=models.CharField(choices=[('Renew', 'Renew'), ('Terminate', 'Terminate'), ('New', 'New')], default='New', help_text='Enter Type', max_length=150),
        ),
    ]
