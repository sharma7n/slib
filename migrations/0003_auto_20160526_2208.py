# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 03:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slib', '0002_auto_20160526_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='days_past_due',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
