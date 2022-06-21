from rest_framework import serializers
from .models import StaffRole,RolesStaff


""" Creating serializers for the role regstration into your system... """
class RoleRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolesStaff
        fields = ['rolename']

""" Creating the serializers the staff role into our system.. """

class StaffData(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = ['role']