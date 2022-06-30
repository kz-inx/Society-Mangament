# Generated by Django 4.0.5 on 2022-06-30 07:43

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0011_alter_dailyvisitorssociety_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyvisitorssociety',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
    ]
