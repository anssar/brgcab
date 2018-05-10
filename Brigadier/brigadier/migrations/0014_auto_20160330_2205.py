# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-30 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brigadier', '0013_auto_20160321_2022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='owner',
            new_name='owner_driver',
        ),
        migrations.AddField(
            model_name='car',
            name='creation_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='brigadier.Service'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner_brigadier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brigadier.Brigadier'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner_model',
            field=models.CharField(choices=[('driver', 'driver'), ('brigadier', 'brigadier')], default='driver', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='creation_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='brigadier.Service'),
        ),
        migrations.AlterField(
            model_name='car',
            name='code',
            field=models.CharField(editable=False, max_length=128),
        ),
    ]
