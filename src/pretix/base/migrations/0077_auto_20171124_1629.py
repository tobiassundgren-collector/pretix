# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-24 16:29
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.translation import ugettext as _

import pretix.base.validators
from pretix.base.i18n import language


def create_checkin_lists(apps, schema_editor):
    Event = apps.get_model('pretixbase', 'Event')
    Checkin = apps.get_model('pretixbase', 'Checkin')
    EventSettingsStore = apps.get_model('pretixbase', 'Event_SettingsStore')
    for e in Event.objects.all():
        locale = EventSettingsStore.objects.filter(object=e, key='locale').first()
        if locale:
            locale = locale.value
        else:
            locale = settings.LANGUAGE_CODE

        if e.has_subevents:
            for se in e.subevents.all():
                with language(locale):
                    cl = e.checkin_lists.create(name=se.name, subevent=se, all_products=True)
                Checkin.objects.filter(position__subevent=se, position__order__event=e).update(list=cl)
        else:
            with language(locale):
                cl = e.checkin_lists.create(name=_('Default list'), all_products=True)
            Checkin.objects.filter(position__order__event=e).update(list=cl)


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0076_orderfee_squashed_0082_invoiceaddress_internal_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(help_text='Should be short, only contain lowercase letters, numbers, dots, and dashes, and must be unique among your events. We recommend some kind of abbreviation or a date with less than 10 characters that can be easily remembered, but you can also choose to use a random value. This will be used in URLs, order codes, invoice numbers, and bank transfer references.', validators=[django.core.validators.RegexValidator(message='The slug may only contain letters, numbers, dots and dashes.', regex='^[a-zA-Z0-9.-]+$'), pretix.base.validators.EventSlugBanlistValidator()], verbose_name='Short form'),
        ),
        migrations.AlterField(
            model_name='eventmetaproperty',
            name='name',
            field=models.CharField(db_index=True, help_text='Can not contain spaces or special characters except underscores', max_length=50, validators=[django.core.validators.RegexValidator(message='The property name may only contain letters, numbers and underscores.', regex='^[a-zA-Z0-9_]+$')], verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='organizer',
            name='slug',
            field=models.SlugField(help_text='Should be short, only contain lowercase letters, numbers, dots, and dashes. Every slug can only be used once. This is being used in URLs to refer to your organizer accounts and your events.', validators=[django.core.validators.RegexValidator(message='The slug may only contain letters, numbers, dots and dashes.', regex='^[a-zA-Z0-9.-]+$'), pretix.base.validators.OrganizerSlugBanlistValidator()], verbose_name='Short form'),
        ),
        migrations.CreateModel(
            name='CheckinList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190)),
                ('all_products', models.BooleanField(default=True, verbose_name='All products (including newly created ones)')),
            ],
        ),
        migrations.AddField(
            model_name='checkinlist',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkin_lists', to='pretixbase.Event'),
        ),
        migrations.AddField(
            model_name='checkinlist',
            name='subevent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, null=True, blank=True, related_name='checkin_lists', to='pretixbase.SubEvent'),
        ),
        migrations.AddField(
            model_name='checkinlist',
            name='limit_products',
            field=models.ManyToManyField(blank=True, to='pretixbase.Item', verbose_name='Limit to products'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checkins', to='pretixbase.CheckinList'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checkins', to='pretixbase.CheckinList'),
        ),
        migrations.AlterField(
            model_name='checkinlist',
            name='subevent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pretixbase.SubEvent', verbose_name='Date'),
        ),
        migrations.RunPython(
            create_checkin_lists,
            migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='checkin',
            name='list',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.PROTECT, related_name='checkins', to='pretixbase.CheckinList'),
        ),
    ]
