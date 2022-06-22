""" Importing libraries """
from rest_framework import serializers
from .models import UserCompliant
from resident.models import UserRole

""" Creating the serializers for the user can filed compliant """
class UserFileCompliantSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserCompliant
        fields = ['title', 'subject']


""" User complain can see by the admin of the system only """
class SeeCompliantSerializers(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    house_no = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.id

    def get_house_no(self, obj):
        return UserRole.objects.get(user=obj.user).house_no

    class Meta:
        model = UserCompliant
        fields = ['id','title','subject','user','status', 'house_no']
        # fields = '__all__'