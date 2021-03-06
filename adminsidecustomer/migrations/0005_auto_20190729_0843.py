# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-29 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsidecustomer', '0004_auto_20190717_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='contract_accepted',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Contract Accepted', max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='contract_sent',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Contract Sent', max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='devices_received',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Devices Received ', max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='devices_shipped',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Devices Shipped ', max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='first_payment_done',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter First Payment Done', max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='installation_date',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Installation Date', max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='installation_done',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Installation Done', max_length=150),
        ),
        migrations.AlterField(
            model_name='customeraccountstatus',
            name='req_has_been_sent',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Req has been sent', max_length=150),
        ),
        migrations.AlterField(
            model_name='customerinvoicemap',
            name='end_term',
            field=models.CharField(choices=[('True', 'T'), ('False', 'F')], default='T', help_text='Enter End Term', max_length=150),
        ),
        migrations.AlterField(
            model_name='sales_tax',
            name='is_fedral_tax',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Fedral Tax', max_length=150),
        ),
        migrations.AlterField(
            model_name='sales_tax',
            name='is_provisional_tax',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Provisional Tax', max_length=150),
        ),
        migrations.AlterField(
            model_name='sales_tax',
            name='is_tax_number_show',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='False', help_text='Enter Tax Number Show', max_length=150),
        ),
    ]
