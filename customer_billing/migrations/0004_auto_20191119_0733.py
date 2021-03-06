# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-19 07:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminsidecustomer', '0017_auto_20191119_0733'),
        ('customer_billing', '0003_auto_20191118_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankingDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_id', models.CharField(max_length=255)),
                ('institution_no', models.CharField(max_length=255)),
                ('account_no', models.CharField(max_length=255)),
                ('account_name', models.CharField(max_length=255)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminsidecustomer.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(choices=[('VISA', 'VISA'), ('MASTERCARD', 'MASTERCARD'), ('AMERICAN EXPRESS', 'AMERICAN EXPRESS')], max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=50)),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminsidecustomer.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='PaypalDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminsidecustomer.Customer')),
            ],
        ),
        migrations.AlterField(
            model_name='billingdetailscustomer',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'CASH'), ('CREDIT CARD', 'CREDIT CARD'), ('BANK DEPOSIT', 'BANK DEPOSIT'), ('PAYPAL', 'PAYPAL')], default='CREDIT CARD', max_length=50),
        ),
    ]
