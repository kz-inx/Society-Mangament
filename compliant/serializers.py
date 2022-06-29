""" Importing libraries """
from rest_framework import serializers
from .models import UserCompliant
from resident.models import UserRole

class UserFileCompliantSerializers(serializers.ModelSerializer):
    """
    User complain can see by the admin of the system only
    """
    class Meta:
        model = UserCompliant
        fields = ['title', 'subject']



class SeeCompliantSerializers(serializers.ModelSerializer):
    """
    User complain can see by the admin of the system only
    """
    # user = serializers.SerializerMethodField()
    house_no = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.id

    def get_house_no(self, obj):
        return UserRole.objects.get(user=obj.user).house_no

    class Meta:
        model = UserCompliant
        fields = ['id','title','subject','user','status', 'house_no']
