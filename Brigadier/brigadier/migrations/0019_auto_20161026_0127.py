# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-25 20:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brigadier', '0018_auto_20161026_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='group',
        ),
        migrations.AddField(
            model_name='crew',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brigadier.CrewGroup'),
        ),
    ]
