""" Importing Libraries """
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserListSerializer, UserPayMaintenanceSerializers, AdminSeeAllMaintenanceRecordsSerializers
from .models import UserRole, UserPayMaintenance
from .message import UserNotGiven, UserStatus, UserAlreadyVerified, SuccessfullyPaid, ErrorOccur, AlreadyPaid, NotUser
import stripe
from django.shortcuts import render

stripe.api_key = 'sk_test_51LHhAgSFfGW1sF18frp7b8yqNOVyHwkSgzxvfT8aHgugxQxcoChSxVud8Sg6lzJZB55ZkezAFWTqPpE9l855D8GN00ovX9Egb8'


class UserListView(ListAPIView):
    """
    Admin of the system has only accessed no other one try to call this else error will raise into the system
    Admin will see user whose status is_verified is false
    """
    permission_classes = [IsAdminUser]
    queryset = UserRole.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = UserRole.objects.filter(is_verfied=False)
        return queryset


class UserStatusUpdate(APIView):
    """
    Admin will update the status and give the permission to the user access the application
    admin of system is able be use this feature no one else has right to perform this operation into the system
    Request Post:
        Http Request
        Admin need the user_id for the updating the status of user into the system
    Response Objects:
        if everything will goes ok status will update and show success msg to the admin
        if error is raise any type it will going to raise exception and error msgs
    """
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        user_id = request.data.get('id')
        user = UserRole.objects.filter(id=user_id).first()
        if user is None:
            return Response({'msg': UserNotGiven}, status=status.HTTP_404_NOT_FOUND)
        elif user.is_verfied:
            return Response({'msg': UserAlreadyVerified}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_verfied = True
            user.save()
            return Response({'msg': UserStatus}, status=status.HTTP_200_OK)


class UserPayMaintance(APIView):
    """
    User will the pay the maintenance of the society using the endpoint
    user need login into the system to access this endpoint.
    Request Post:
        HTTP.Request
        amount of maintance to the user will display he/she needs pay it
    Request Objects:
        if everything goes okk user pay it and system will show success msg to the user
        if anything found wrong error rise into the system and display to the user
    """
    permission_classes = [IsAuthenticated]
    query_set = UserPayMaintenance.objects.all()

    def post(self, request):
        current_user = request.user
        data = request.data.copy()
        print(data)
        try:
            user_role = UserRole.objects.get(user=current_user)
            print(f"User Role:- {user_role}")
            if user_role:
                currentMonth = datetime.now().month
                currentYear = datetime.now().year
                user_house = user_role.house_no
                data['house_no'] = user_house
                queryset = UserPayMaintenance.objects.filter(house_no=user_house, pay_date__month=currentMonth,
                                                             pay_date__year=currentYear).first()
                if queryset is None:
                    serializers = UserPayMaintenanceSerializers(data=data)
                    if serializers.is_valid(raise_exception=True):
                        payment_method = stripe.PaymentMethod.create(
                            type="card",
                            card={
                                "number": "4242424242424242",
                                "exp_month": 7,
                                "exp_year": 2023,
                                "cvc": "314",
                            },
                        )
                        print(payment_method.id)
                        customer = stripe.Customer.create(
                            email=request.user.email, payment_method=payment_method.id
                        )
                        print(customer, "customer.........")
                        stripe.PaymentIntent.create(
                            customer=customer.id,
                            payment_method=payment_method.id,
                            currency='usd',
                            amount=2500,
                            confirm=True,
                        )
                        serializers.save()
                        return Response({'status': 'pass', 'msg': SuccessfullyPaid}, status=status.HTTP_200_OK)
                    return Response({'status': 'fail', 'msg': ErrorOccur}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'status': 'fail', 'msg': AlreadyPaid}, status=status.HTTP_400_BAD_REQUEST)

        except UserRole.DoesNotExist:
            return Response({'status': 'fail', 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)


class AdminCanSeeAllRecordsMaintance(APIView):
    """
    Admin will see all the records the related to the user pay maintenance into the system
    only admin of the system is has permission to the see user records any else try to this it will show directly error msg
    Request get:
        HTTP Request
        admin need enter month into the system for classfiy the query
    Response Objects:
        Admin will be able to see particular month records into the system
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        month = request.GET.get("month")
        print(month)
        data = UserPayMaintenance.objects.filter(pay_date__month=month)
        # queryset = UserPayMaintenance.objects.all().order_by('-pay_date')
        serializer = AdminSeeAllMaintenanceRecordsSerializers(data, many=True)
        return Response({'status': 'pass', 'data': serializer.data}, status=status.HTTP_200_OK)

def success(request):
    return render(request,'success.html')
