""" Importing Libraries"""
from rest_framework import serializers
from resident.models import UserRole, UserPayMaintenance


class UserDataEnter(serializers.ModelSerializer):
    """
    serializers that will enter the house_no into the system
    """
    class Meta:
        model = UserRole
        fields = ['house_no']

class UserListSerializer(serializers.ModelSerializer):
    """
    serializer for updating the status of the user into the system..
    """
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user_name', 'user_email', 'is_verfied', 'house_no']

class GetUserData(serializers.ModelSerializer):
    """
    Admin will able to see whole profile information of all user
    """
    user_id = serializers.CharField(source="user.id",read_only=True)
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserRole
        fields = ['user_id','user_name','user_email','house_no']


class UserViewProfile(serializers.ModelSerializer):
    """
    User will be able to see his whole profile into the system
    """
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserRole
        fields = ['user_name', 'user_email', 'house_no']

class UserPayMaintenanceSerializers(serializers.ModelSerializer):
    """
    user will be able to pay the maintenance into the system by providing the details
    """
    class Meta:
        model = UserPayMaintenance
        fields = ['house_no','amount_pay']










