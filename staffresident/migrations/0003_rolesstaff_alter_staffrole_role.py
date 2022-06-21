# Generated by Django 4.0.5 on 2022-06-20 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staffresident', '0002_staffrole_change_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='RolesStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rolename', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='staffrole',
            name='role',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='staffresident.rolesstaff'),
        ),
    ]