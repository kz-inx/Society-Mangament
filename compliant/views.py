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
     client should be login into the system for using this service
    Request Post:
        HTTP.Request
        This method will post the given data into the database
        It will also notify the user and as well as admin of the system via email.
    Return Objects:
        It will return msg in json format if will request successfully placed or it will rase error exception
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserFileCompliantSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(user=request.user)
            house_no = request.user.user_data.get().house_no
            user_query = UserRole.objects.filter(house_no=house_no).values("user")
            email_list = User.objects.filter(id__in=user_query).values_list('email', flat=True)
            email_list = [email for email in email_list]
            # print(email_list)
            email_admin = User.objects.filter(is_admin=True).values_list('email', flat=True)
            admin_email = [email for email in email_admin]
            email_list.extend(admin_email)
            # email_list = chain(email_list, email_admin)
            print(email_list)
            send_mail(
                instance.title,
                instance.subject,
                'EMAIL_USER',
                email_list,
                fail_silently=False,
            )
            return Response({'status': 1, 'msg': CompliantFile}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeeCompliantViews(ListAPIView):
    """
    Creating the endpoint to the see the complaints has been filled...
    admin of the system can use this service. If any be one else than admin use access this endpoint it will raise error
     It will show all present complain into the system whose status is false into the system.
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
    Creating class view for the admin to solve the compliant of society member.
    only admin of the system can use this endpoint any one else being will go to use it will raise the error in the system
    Request Post:
        HTTP.Request
        It will take the compliant the id and update the status on it.
        Is also go update the status of compliant has been solved to user via email.
    Return Objects:
        It will return the success msg in format of json and show to user
        or IF complain resolve or not available into the system it will raise the error msg and display in json format
    """
    permission_classes = [IsAdminUser]
    def post(self,request):
        compliant_id = request.data.get('id')
        compliant_id= get_object_or_404(UserCompliant, id=compliant_id)
        user = UserCompliant.objects.filter(id=compliant_id.id).first()

        if user is None:
            return Response({'status':0,'msg':UserNotGiven},status=status.HTTP_404_NOT_FOUND)
        elif user.status:
            return Response({'status':0,'msg':UserAlreadyVerified},status=status.HTTP_400_BAD_REQUEST)
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

            return Response({'status':1,'msg':CompliantStatus}, status=status.HTTP_200_OK)










