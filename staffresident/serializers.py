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

class GetStaffData(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    rolename = serializers.CharField(source="role.rolename")

    class Meta:
        model = StaffRole
        fields = ['user_name','user_email','rolename']