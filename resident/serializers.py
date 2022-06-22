""" Importing Libraries"""
from rest_framework import serializers
from resident.models import UserRole

""" serializers that will enter the house_no into the system """
class UserDataEnter(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['house_no']

""" serializer for updating the status of the user into the system.."""
class UserListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user_name', 'user_email', 'is_verfied', 'house_no']







