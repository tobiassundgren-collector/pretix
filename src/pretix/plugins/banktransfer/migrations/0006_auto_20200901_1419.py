# Generated by Django 3.0.9 on 2020-09-01 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banktransfer', '0005_auto_20181023_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='banktransaction',
            name='bic',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banktransaction',
            name='date_parsed',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='banktransaction',
            name='iban',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
