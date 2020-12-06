# Generated by Django 3.0.9 on 2020-11-23 15:51

from django.db import migrations


def remove_old_settings(app, schema_editor):
    EventSettingsStore = app.get_model('pretixbase', 'Event_SettingsStore')

    EventSettingsStore.objects.filter(key__startswith='payment_', key__endswith='__hidden_url').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0169_checkinlist_gates'),
    ]

    operations = [
        migrations.RunPython(remove_old_settings, migrations.RunPython.noop)
    ]
