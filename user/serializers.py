from django.contrib.auth import password_validation
from rest_framework import serializers
from user.models import User
from resident.models import UserRole

""" Creating serializer for regstration the normal user into your system """
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, data):
        password_validation.validate_password(password=data)
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

""" User login view serializers fetching the data from the database"""
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

""" User change password serilaizers takeing two  password change init"""
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        password_validation.validate_password(password=password)
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.password_change = True
        user.save()
        return attrs

""" User Profile view from the system.."""
class UserProfileSerializer(serializers.ModelSerializer):
    house_no = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'name', 'house_no']

    def get_house_no(self, obj):
        return obj.user_data.get().house_no