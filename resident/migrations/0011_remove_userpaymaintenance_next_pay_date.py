# Generated by Django 4.0.5 on 2022-07-01 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0010_alter_userpaymaintenance_pay_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpaymaintenance',
            name='next_pay_date',
        ),
    ]
