""" Importing the libraries for creating models """
from django.db import models
from user.models import User

# Create your models here.
""" creating the user file compliant model with the necessary fields"""
class UserCompliant(models.Model):
    title = models.CharField(max_length=150)
    subject = models.CharField(max_length=1000)
    user = models.ForeignKey(User,default=None, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)