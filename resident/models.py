""" Importing Libraries"""
from django.db import models
from user.models import User
# Create your models here.

""" creating a model for entering the data into system...."""
class UserRole(models.Model):
    user = models.ForeignKey(User,default=None, on_delete=models.CASCADE, related_name='user_data')
    is_verfied = models.BooleanField(default=False)
    house_no = models.CharField(max_length=50)
