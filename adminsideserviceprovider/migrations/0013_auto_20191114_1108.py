# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-14 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminsideserviceprovider', '0012_auto_20191114_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerticketscategoriesmap',
            name='service_provider',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='adminsideserviceprovider.ServiceProvider'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customerservicecontract',
            name='type',
            field=models.CharField(choices=[('Terminate', 'Terminate'), ('Renew', 'Renew'), ('New', 'New')], default='New', help_text='Enter Type', max_length=150),
        ),
    ]