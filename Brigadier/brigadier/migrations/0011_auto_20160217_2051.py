# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-17 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brigadier', '0010_auto_20160217_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crewgroup',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigadier.Service'),
        ),
    ]
