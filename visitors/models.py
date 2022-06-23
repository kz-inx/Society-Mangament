from django.db import models

from resident.models import UserRole
from user.models import User
from staffresident.models import StaffRole
# Create your models here.

class VisitorsSociety(models.Model):

    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    house_no = models.CharField(max_length=25)
    visitors_Status = [
        ('Accepted', 'Accepted'),
        ('Reject', 'Reject'),
        ('Unverified','Unverified'),
    ]
    is_status = models.CharField(choices=visitors_Status, default='Unverified', max_length=15)
    user = models.ForeignKey(UserRole,default=None, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(StaffRole, default=None, on_delete=models.CASCADE, null=True)