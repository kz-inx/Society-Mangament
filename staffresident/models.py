""" Importing Libraries"""
from django.db import models
from user.models import User


# Create your models here.
class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }
    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)

class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass

""" Creating the database of the role mode in the our system """
class RolesStaff(models.Model):
    rolename = CICharField(max_length=50, unique=True)

""" Creating the database of the staff-account in the our system """
class StaffRole(models.Model):
    user = models.ForeignKey(User,default=None, on_delete=models.CASCADE)
    role = models.ForeignKey(RolesStaff, default=None, on_delete=models.CASCADE, related_name='staff_data')
    change_password = models.BooleanField(default=False)
