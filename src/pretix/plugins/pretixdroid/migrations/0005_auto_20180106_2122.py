# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-06 21:22
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixdroid', '0004_auto_20171124_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='appconfiguration',
            name='app',
            field=models.CharField(choices=[('pretixdroid', 'pretixdroid – for Android smartphones'), ('pretixdesk', 'pretixdesk – for desktop computers')], default='pretixdroid', max_length=190, verbose_name='Scan software'),
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='allow_search',
            field=models.BooleanField(default=True, help_text='If disabled, the device can not search for attendees by name. pretixdroid 1.6 or pretixdesk only.', verbose_name='Search allowed'),
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.CheckinList', verbose_name='Check-in list'),
        ),
        migrations.AlterField(
            model_name='appconfiguration',
            name='show_info',
            field=models.BooleanField(default=True, help_text='If disabled, the device can not see how many tickets exist and how many are already scanned. pretixdroid 1.6 or pretixdesk only.', verbose_name='Show information'),
        ),
    ]