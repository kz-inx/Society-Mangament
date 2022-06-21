""" Importing the libraries"""
from django.db import models
from user.models import User

# Create your models here.

""" creating the notifcation model to store data related to it"""


class Notifcation(models.Model):
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=600)
    house_no = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


