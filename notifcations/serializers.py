""" Importing the libraries """
from rest_framework import serializers
from .models import Notifcation

""" Creating the serializers admin sent notifcation to all user of the system """
class AdminNotifcationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notifcation
        fields = ['title', 'message']

""" Creating the serializers admin sent notifcation to particular user in the system"""
class AdminNotifcationParticularSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notifcation
        fields = ['title', 'message','house_no']