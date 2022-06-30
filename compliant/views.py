""" Importing libraries """
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import send_mail
from resident.models import UserRole
from user.models import User
from .serializers import UserFileCompliantSerializers, SeeCompliantSerializers
from .message import CompliantFile, UserNotGiven, UserAlreadyVerified, CompliantStatus
from .models import UserCompliant
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, get_object_or_404

class UserFileCompliant(APIView):
    """
    Creating the views for file compliant for particular user ...
    """
    permission_classes = [IsAuthenticated]

    def post (self, request):
        serializer = UserFileCompliantSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(user=request.user)
            house_no = request.user.user_data.get().house_no
            user_query = UserRole.objects.filter(house_no=house_no).values("user")
            email_list = User.objects.filter(id__in=user_query).values_list('email', flat=True)
            print(email_list)
            send_mail(
                instance.title,
                instance.subject,
                'EMAIL_USER',
                email_list,
                fail_silently=False,
            )
            return Response({'status': 'Successfully', 'msg': CompliantFile}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeeCompliantViews(ListAPIView):
    """
    Creating the endpoint to the see the complaints has been filled...
     """
    permission_classes = [IsAdminUser]

    queryset = UserCompliant.objects.all()
    serializer_class = SeeCompliantSerializers

    def get_queryset(self):
        queryset = UserCompliant.objects.filter(status=False)
        print(f"QUERY SET {queryset}")
        return queryset


class AdminUpdateStatusCompliant(APIView):
    """
    Creating class view for the admin to solve the compliant of society member
    """
    permission_classes = [IsAdminUser]
    def post(self,request):
        compliant_id = request.data.get('id')
        compliant_id= get_object_or_404(UserCompliant, id=compliant_id)
        user = UserCompliant.objects.filter(id=compliant_id.id).first()

        if user is None:
            return Response({'status':'Not available','msg':UserNotGiven},status=status.HTTP_404_NOT_FOUND)
        elif user.status:
            return Response({'status':'Already Solved','msg':UserAlreadyVerified},status=status.HTTP_400_BAD_REQUEST)
        else:
            user.status = True
            user.save()
            house_no = request.user.user_data.get().house_no
            user_query = UserRole.objects.filter(house_no=house_no).values("user")
            email_list = User.objects.filter(id__in=user_query).values_list('email', flat=True)
            print(email_list)
            send_mail(
                "Compliant has been solved",
                "Secretary of society has been solved your complain. This Message regarding you update the status of your compliant",
                'EMAIL_USER',
                email_list,
                fail_silently=False,
            )

            return Response({'status':'Solved','msg':CompliantStatus}, status=status.HTTP_200_OK)










