# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-01 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsideserviceprovider', '0006_auto_20190803_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerservicecontract',
            name='type',
            field=models.CharField(choices=[('New', 'New'), ('Terminate', 'Terminate'), ('Renew', 'Renew')], default='New', help_text='Enter Type', max_length=150),
        ),
    ]
