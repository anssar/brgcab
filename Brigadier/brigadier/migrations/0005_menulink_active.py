# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-23 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brigadier', '0004_controlpair_menulink'),
    ]

    operations = [
        migrations.AddField(
            model_name='menulink',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
