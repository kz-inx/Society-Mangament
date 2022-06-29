from rest_framework import serializers
from .models import StaffRole,RolesStaff


""" Creating serializers for the role regstration into your system... """
class RoleRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolesStaff
        fields = ['rolename']

class StaffData(serializers.ModelSerializer):
    """
    Creating the serializers the staff role into our system..
     """
    class Meta:
        model = StaffRole
        fields = ['role']

class GetStaffData(serializers.ModelSerializer):
    """
    Admin will see the profile and maintain the staff profile
    """
    user_id = serializers.CharField(source="user.id",read_only=True)
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    rolename = serializers.CharField(source="role.rolename")

    class Meta:
        model = StaffRole
        fields = ['user_id','user_name','user_email','rolename']

class StaffViewProfile(serializers.ModelSerializer):
    """
    Staff will be able to see his whole profile into the system
    """
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    rolename = serializers.CharField(source="role.rolename")

    class Meta:
        model = StaffRole
        fields = ['user_name','user_email','rolename']


