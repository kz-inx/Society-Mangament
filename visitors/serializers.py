""" Importing Libraries"""
from rest_framework import serializers
from .models import VisitorsSociety

class VisitorsRegisterSerializers(serializers.ModelSerializer):
    """
    creating a serializers for the register visitors into the system
    """
    staff = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = VisitorsSociety
        fields = ['name','phone_number','house_no', 'staff']

class SeeVisitorsSerializers(serializers.ModelSerializer):
    """
    creating a serializers for view visitors come meet particular user of the system
    """
    class Meta:
        model = VisitorsSociety
        fields = ['id','name','phone_number']

class StaffSeeAllVisitorsSerializers(serializers.ModelSerializer):
    """
    Creating a serializers for the staff view visitors has been arrived into the society
    """
    class Meta:
        model = VisitorsSociety
        fields = ['id', 'name','phone_number','is_status','date_posted']

class UserSeeAllVisitorsSerializers(serializers.ModelSerializer):
    """
    creating a serializers for the user view see visitors has been arrived into there home
    """
    class Meta:
        model = VisitorsSociety
        fields = ['name','phone_number','is_status','date_posted']



