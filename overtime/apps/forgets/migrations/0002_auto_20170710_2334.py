# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-10 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forget',
            name='new_password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]