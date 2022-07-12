""" Importing Libraries """
import datetime as DT
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from staffresident.models import StaffRole
from .serializers import VisitorsRegisterSerializers, SeeVisitorsSerializers, StaffSeeAllVisitorsSerializers, \
    UserSeeAllVisitorsSerializers, DailyVistiorsSerializers, StaffVerifyDailyVisitors,AdminSeeDailyVisitorsRecord
from .models import VisitorsSociety
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from user.models import User
from resident.models import UserRole
from .models import DailyVisitorsSociety
from .message import VerfiyVistiors, NotStaff, NotUser, VistiorsNotAvailable, VisitorsStatus, \
    VisitorIsAllAlreadyVerfied, PasswordChangePending, VisitorsRegstration, VisitorsRegstrationFail


class AdminSentNotifcationParticular(APIView):
    """
    creating a apiview to sent the notifcation to the user which visitors has come to meet him
    staff need login into the system to access this endpoint. Any other than staff will try it will throw the error
    Request post:
        Http Request
        staff needs to fill the necessary details like visitors name, phone number etc..
    Response Objects:
        If everything goes right it will sent mail to the user related visitors information
        if anything goes wrong it going raise exception into the system
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user
        try:
            staff_role = StaffRole.objects.get(user=current_user)
            if staff_role.change_password:
                serializer = VisitorsRegisterSerializers(data=request.data, context={'request': self.request})
                if serializer.is_valid(raise_exception=True):
                    staffaccount = StaffRole.objects.get(user=self.request.user)
                    notifcation = serializer.save(staff=staffaccount)
                    print(f"notifcation recieve {notifcation}")
                    house_no = notifcation.house_no
                    user_query = UserRole.objects.filter(house_no=house_no).values("user")
                    email_list = User.objects.filter(id__in=user_query).values_list('email', flat=True)
                    print(f"email_list:- {email_list}")
                    send_mail(
                        'Visitors Verify mail',
                        notifcation.name,
                        'EMAIL_USER',
                        email_list,
                        fail_silently=False,
                    )
                    return Response({'status': 1, 'msg': VerfiyVistiors}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': 0, 'msg': PasswordChangePending}, status=status.HTTP_400_BAD_REQUEST)

        except StaffRole.DoesNotExist:
            return Response({'status': 0, 'msg': NotStaff}, status=status.HTTP_400_BAD_REQUEST)


class SeeVisitors(ListAPIView):
    """
    creating a endpoint where user come see which visitors has come meet him
    user need login into the system for view this endpoint. This endpoint is only accessible by user only
    Any other will try to access it will throw the error
    Request Get:
        Http request
        user will able to show visitors name how came meet him
    Response objects:
        user will be able to see visitors everything is ok
        if anything will go wrong it will raise the error
    """
    permission_classes = [IsAuthenticated]
    query_set = VisitorsSociety.objects.all()
    serializer_class = SeeVisitorsSerializers

    def get(self, request):
        try:
            current_user = request.user
            resident_user = UserRole.objects.get(user=current_user)
            if resident_user:
                userrole = UserRole.objects.get(user=self.request.user)
                queryset = VisitorsSociety.objects.filter(Q(house_no=userrole.house_no) & Q(is_status='Unverified'))
                serialized_data = SeeVisitorsSerializers(queryset, many=True)
                return Response({'data': serialized_data.data})
        except Exception as e:
            print(e, type(e))
            return Response({'status': 0, 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)


class UpdateStatusVisitors(APIView):
    """
    creating a class will visitors will verify or reject the visitors and staff will notify via email
    user need login into the system for view this endpoint. This endpoint is only accessible by user only
    Any other will try to access it will throw the error
    Request Post:
        Http.Request
        user need update the status of visitors using id. where id is pk
    Response.Objects:
        if everything's goes correct it will msg staff related status of visitors
        if anything goes wrong will raise the error msg in from the json data
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        current_user = request.user
        print(f"Current user is:- {current_user}")
        # print(request.user.id)
        try:
            staff_role = UserRole.objects.get(user=current_user)
            if staff_role:
                visitor_id = request.data.get('id')
                visitor_id = get_object_or_404(VisitorsSociety, id=visitor_id)
                visitor_status = request.data.get('is_status')
                user_id = request.user.user_data.get()
                visitor = VisitorsSociety.objects.get(id=visitor_id.id)
                visitor.is_status = visitor_status
                visitor.user = user_id
                if not visitor.is_answer:
                    visitor.is_answer = True
                    visitor.save()
                    staff = visitor.staff
                    staff_email = staff.user.email
                    send_mail(
                        'Status Update Related Visitors',
                        visitor_status,
                        'EMAIL_USER',
                        [staff_email],
                        fail_silently=False,
                    )
                    if visitor is None:
                        return Response({'status': 0, 'msg': VistiorsNotAvailable},
                                        status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({'status': 1, 'msg': VisitorsStatus}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'Not available', 'msg': VisitorIsAllAlreadyVerfied},
                                    status=status.HTTP_404_NOT_FOUND)

        except UserRole.DoesNotExist:
            return Response({'status': 0, 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)


class StaffSeeAllVisitors(APIView):
    """
    Staff can see all the visitors come into the society into the last seven days.
    staff need login into the system to access this endpoint. Any other than staff will try it will throw the error
    Request get:
        Http Request
        staff needs login into the system for view this
    Response Objects:
        if everything go ok staff able to see all visitors visit in society in last one week
        if anything will go wrong it wil raise exception error
    """
    permission_classes = [IsAuthenticated]
    query_set = VisitorsSociety.objects.all()
    serializer_class = StaffSeeAllVisitorsSerializers

    def get(self, request):
        try:
            current_user = request.user
            staff_role = StaffRole.objects.get(user=current_user)
            if staff_role.change_password:
                today = DT.date.today()
                week_ago = today - DT.timedelta(days=7)
                queryset = VisitorsSociety.objects.filter(date_posted__gte=week_ago)
                serialized_data = StaffSeeAllVisitorsSerializers(queryset, many=True)
                return Response({'data': serialized_data.data})
            return Response({'status': 0, 'msg': PasswordChangePending}, status=status.HTTP_400_BAD_REQUEST)

        except StaffRole.DoesNotExist:
            return Response({'status': 0, 'msg': NotStaff}, status=status.HTTP_400_BAD_REQUEST)


class UserSeeAllVisitors(APIView):
    """
    User can see all the visitors come into the society into the last seven days
    user need login into the system to access this endpoint. Any other than user will try it will throw the error
    Request get:
        Http Request
        user needs login into the system for view this
    Response Objects:
        if everything go ok user able to see all visitors visit in society in last one week
        if anything will go wrong it wil raise exception error
    """
    permission_classes = [IsAuthenticated]
    query_Set = VisitorsSociety.objects.all()
    serializer_class = UserSeeAllVisitorsSerializers

    def get(self, request):
        try:
            current_user = request.user
            resident_user = UserRole.objects.get(user=current_user)
            if resident_user:
                user_role = UserRole.objects.get(user=self.request.user)
                today = DT.date.today()
                week_ago = today - DT.timedelta(days=7)
                queryset = VisitorsSociety.objects.filter(Q(house_no=user_role.house_no) & Q(date_posted__gte=week_ago))
                serialized_data = UserSeeAllVisitorsSerializers(queryset, many=True)
                return Response({'data': serialized_data.data})
        except UserRole.DoesNotExist:
            return Response({'status': 0, 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)


class DailyVisitorsRegister(APIView):
    """
    creating a view where admin will register the daily visitors into the system
    Admin of the system is able to see this records another will try it will go throw the errors
    Request post:
        Http request
        admin needs fills all details which needs the require into the database
    Return Object:
        Everything's goes okk then user will register into the database
        if anything goes wrong it will raise error in the form json data
    """
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = DailyVistiorsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': 1, 'msg': VisitorsRegstration}, status=status.HTTP_201_CREATED)
        return Response({'status': 0, 'msg': VisitorsRegstrationFail}, status=status.HTTP_400_BAD_REQUEST)


class DailyVisitorsVerify(APIView):
    """
    Creating a view for staff where they can verify the regular visitors into the society
    staff role of the system has permission any other will try it will go to throw the errors
    Request get:
        Http Request
        staff needs enters id into the required to be filed
    Response Objects:
        If id right then all the information will display of staff
        If id not available or anything will go wrong into the system it will go the raise error msg in format json
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, serial_id):
        current_user = request.user
        try:
            staff_role = StaffRole.objects.get(user=current_user)
            if staff_role.change_password:
                daily_visitor_query = get_object_or_404(DailyVisitorsSociety, serial_id=serial_id)
                serializer = StaffVerifyDailyVisitors(daily_visitor_query)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response({'status': 0, 'msg': PasswordChangePending}, status=status.HTTP_400_BAD_REQUEST)

        except StaffRole.DoesNotExist:
            return Response({'status': 1, 'msg': NotStaff}, status=status.HTTP_400_BAD_REQUEST)

class AdminSeeDailyVisitors(ListAPIView):
    """
    Admin of the system is able to see all the records daily visitors into the society
    Admin of the system is able to see this records another will try it will go throw the errors
    Admin is able to see all the records of daily visitors with the necessary information needed
    """
    permission_classes = [IsAdminUser]
    queryset = DailyVisitorsSociety.objects.all()
    serializer_class = AdminSeeDailyVisitorsRecord


















