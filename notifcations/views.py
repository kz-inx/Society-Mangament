""" Importing Libraries """
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import AdminNotifcationSerializers, AdminNotifcationParticularSerializers
from .models import Notifcation
from .message import SentNotifcation, SentParticularUser
from django.db.models import Q
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.core.mail import send_mail
from user.models import User
from resident.models import UserRole

class AdminSentNotifcationAll(APIView):
    """
     Send Notifications to all user in the system
     admin of the system should login into the system if any else try it will go throw error msg
     Request Post:
        Http Request
        admin need passes the subject and message to the system
    Response Objects:
        if everything goes ok user will notify by the mail the new notifications
        if anything's fails it will raise exception the error and show msg in the form json data
        it will send notifications to all user of the system
     """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminNotifcationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            notifcation = serializer.save()
            user_query = UserRole.objects.all().values("user")
            email_list = User.objects.filter(id__in=user_query).values_list('email', flat=True)
            send_mail(
                notifcation.title,
                notifcation.message,
                'EMAIL_USER',
                email_list,
                fail_silently=False,
            )
            return Response({'status':'Successfully','msg': SentNotifcation}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSentNotifcationParticular(APIView):
    """
    Send notifications to particular user in the system
    admin of the system should log in into the system if any else try it will go throw error msg
     Request Post:
        Http Request
        admin need passes the subject and message to the system
    Response Objects:
        if everything goes ok user will notify by the mail the new notifications
        if anything's fails it will raise exception the error and show msg in the form json data
        it will send notifications to particular user of the system
    """
    permission_classes = [IsAdminUser]

    def post(self,request):
        serializer = AdminNotifcationParticularSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            notifcation = serializer.save()
            house_no = notifcation.house_no
            user_query = UserRole.objects.filter(house_no=house_no).values("user")
            email_list = User.objects.filter(id__in=user_query).values_list('email', flat=True)
            send_mail(
                notifcation.title,
                notifcation.message,
                'EMAIL_USER',
                email_list,
                fail_silently=False,
            )
            return Response({'status':'Successfully','msg': SentParticularUser}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeeNotifcation(ListAPIView):
    """
     user will be see the notifcation into the system
     User should be login into the system before accessing this endpoints
     User will be able to see all notifications of that he/she received into the system
     the notifications shows to user on descending order manner
     """
    permission_classes = [IsAuthenticated]
    queryset = Notifcation.objects.all()
    serializer_class = AdminNotifcationSerializers
    def get_queryset(self):
        userrole = UserRole.objects.get(user=self.request.user)
        queryset = Notifcation.objects.filter(Q(house_no=userrole.house_no) | Q(house_no="")).order_by('-created_at')
        return queryset

