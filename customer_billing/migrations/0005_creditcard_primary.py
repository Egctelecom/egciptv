# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-19 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_billing', '0004_auto_20191119_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]