# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 17:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slib', '0005_holding_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holding',
            name='code',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='number',
            field=models.SmallIntegerField(default=0, editable=False),
        ),
    ]
