""" Importing Libraries """
from django.db import models
from django.utils import timezone
from resident.models import UserRole
from staffresident.models import StaffRole

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
    is_answer = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)