# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-18 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsideserviceprovider', '0014_auto_20191118_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerservicecontract',
            name='type',
            field=models.CharField(choices=[('Terminate', 'Terminate'), ('New', 'New'), ('Renew', 'Renew')], default='New', help_text='Enter Type', max_length=150),
        ),
    ]
