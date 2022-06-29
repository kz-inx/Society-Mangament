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
     See notification by the user on there particular endpoint
     """
    permission_classes = [IsAuthenticated]
    queryset = Notifcation.objects.all()
    serializer_class = AdminNotifcationSerializers
    def get_queryset(self):
        userrole = UserRole.objects.get(user=self.request.user)
        queryset = Notifcation.objects.filter(Q(house_no=userrole.house_no) | Q(house_no="")).order_by('-created_at')
        return queryset

