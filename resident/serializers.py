from rest_framework import serializers
from resident.models import UserRole

class UserDataEnter(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['house_no']


class UserListSerializer(serializers.ModelSerializer):
    user_name= serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = UserRole
        fields = ['id','user_name','user_email','is_verfied','house_no']