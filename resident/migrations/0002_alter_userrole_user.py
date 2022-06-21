# Generated by Django 4.0.5 on 2022-06-21 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resident', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to=settings.AUTH_USER_MODEL),
        ),
    ]
