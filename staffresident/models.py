""" Importing Libraries"""
from django.db import models
from user.models import User

# Create your models here.

""" Creating the database of the role mode in the our system """
class RolesStaff(models.Model):
    rolename = models.CharField(max_length=50, unique=True)

""" Creating the database of the staff-account in the our system """
class StaffRole(models.Model):
    user = models.ForeignKey(User,default=None, on_delete=models.CASCADE)
    role = models.ForeignKey(RolesStaff, default=None, on_delete=models.CASCADE, related_name='staff_data')
    change_password = models.BooleanField(default=False)
