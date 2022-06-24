""" Importing Libraries"""
from rest_framework import serializers
from .models import VisitorsSociety

""" creating a serializers for the register visitors into the system """
class VisitorsRegisterSerializers(serializers.ModelSerializer):
    staff = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = VisitorsSociety
        fields = ['name','phone_number','house_no', 'staff']

""" creating a serializers for view visitors come meet particular user of the system"""
class SeeVisitorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = VisitorsSociety
        fields = ['id','name','phone_number']

""" creating a serializers for updating the status of the visitors its done by the user only...."""



