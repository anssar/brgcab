# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brigadier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128)),
                ('mark', models.CharField(max_length=128)),
                ('color', models.CharField(max_length=128)),
                ('gos_number', models.CharField(max_length=128)),
                ('car_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balans', models.IntegerField()),
                ('blocked', models.BooleanField()),
                ('online', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=128)),
                ('mobile_phone', models.CharField(max_length=128)),
                ('driver_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='brigadier',
            name='group_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crew',
            name='brigadier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigadier.Brigadier'),
        ),
        migrations.AddField(
            model_name='crew',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigadier.Car'),
        ),
        migrations.AddField(
            model_name='crew',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brigadier.Driver'),
        ),
    ]
