""" Importing Libraries"""
from rest_framework import serializers
from .models import VisitorsSociety, DailyVisitorsSociety


class VisitorsRegisterSerializers(serializers.ModelSerializer):
    """
    creating a serializers for the register visitors into the system
    """
    staff = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = VisitorsSociety
        fields = ['name', 'phone_number', 'house_no', 'staff']


class SeeVisitorsSerializers(serializers.ModelSerializer):
    """
    creating a serializers for view visitors come meet particular user of the system
    """

    class Meta:
        model = VisitorsSociety
        fields = ['id', 'name', 'phone_number']


class StaffSeeAllVisitorsSerializers(serializers.ModelSerializer):
    """
    Creating a serializers for the staff view visitors has been arrived into the society
    """

    class Meta:
        model = VisitorsSociety
        fields = ['id', 'name', 'phone_number', 'is_status', 'date_posted']


class UserSeeAllVisitorsSerializers(serializers.ModelSerializer):
    """
    creating a serializers for the user view see visitors has been arrived into there home
    """

    class Meta:
        model = VisitorsSociety
        fields = ['name', 'phone_number', 'is_status', 'date_posted']


class DailyVistiorsSerializers(serializers.ModelSerializer):
    """
    creating a serializers for the new daily visitors into the society register into the system
    """

    class Meta:
        model = DailyVisitorsSociety
        fields = ['serial_id', 'name', 'phone_number', 'profile_pics', 'addharcard_number']


class StaffVerifyDailyVisitors(serializers.ModelSerializer):
    """
    Sending Data to the staff verfiy the visitors of given ID
    """

    class Meta:
        model = DailyVisitorsSociety
        fields = ['name', 'phone_number', 'profile_pics']

class AdminSeeDailyVisitorsRecord(serializers.ModelSerializer):
    """
    Admin is able to see all the records of daily staff visitors into the society
    """
    class Meta:
        model = DailyVisitorsSociety
        fields = ['name','phone_number','profile_pics','addharcard_number']