""" Importing Libraries """
import os
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from societymangament import settings
from .serializers import UserListSerializer, UserPayMaintenanceSerializers, \
    AdminSeeAllMaintenanceRecordsSerializers, AdminUpdateAmountMiantanceSerializers
from .models import UserRole, UserPayMaintenance, AmountPayMaintenance
from .message import UserNotGiven, UserStatus, UserAlreadyVerified, SuccessfullyPaid, ErrorOccur, AlreadyPaid, NotUser, \
    AmountUpdate
import stripe
from django.shortcuts import render
from dotenv import load_dotenv
load_dotenv()

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
        if not user :
            return Response({'status': 0, 'msg': UserNotGiven}, status=status.HTTP_404_NOT_FOUND)
        elif user.is_verfied:
            return Response({'status': 0, 'msg': UserAlreadyVerified}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_verfied = True
            user.save()
            return Response({'status': 1, 'msg': UserStatus}, status=status.HTTP_200_OK)


class UserNormalPayMaintance(APIView):
    """
    User will the pay the maintenance of the society using the endpoint
    user need login into the system to access this endpoint.
    Request Post:
        HTTP.Request
        amount of maintance to the user will display he/she needs pay it
    Requests Objects:
        if everything goes okk user pay it and system will show success msg to the user
        if anything found wrong error rise into the system and display to the user
    """
    permission_classes = [IsAuthenticated]
    query_set = UserPayMaintenance.objects.all()

    def post(self, request):
        current_user = request.user
        data = request.data.copy()
        try:
            user_role = UserRole.objects.get(user=current_user)
            if user_role:
                currentMonth = datetime.now().month
                currentYear = datetime.now().year
                currentday = datetime.now().day
                user_house = user_role.house_no
                data['house_no'] = user_house
                data['is_complete_pay'] = True
                # amount_mqintenance = AmountPayMaintenance.objects.all().only("amount_pay").first()
                amount_mqintenance = 2560
                if currentday >= 5:
                    peresent_day = currentday - 5
                    fine_amount = peresent_day * 100
                    print(fine_amount)
                    # amount_pay = fine_amount+int(amount_mqintenance.amount_pay)
                    amount_pay = fine_amount + int(amount_mqintenance)
                else:
                    # amount_pay=int(amount_mqintenance.amount_pay)
                    amount_pay = int(amount_mqintenance)
                data['amount_pay']= amount_pay
                queryset = UserPayMaintenance.objects.filter(house_no=user_house, pay_date__month=currentMonth,
                                                             pay_date__year=currentYear).first()
                if queryset is None:
                    serializers = UserPayMaintenanceSerializers(data=data)
                    print(f"serial {serializers}")
                    if serializers.is_valid(raise_exception=True):
                        session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            line_items=[{
                                'price_data': {
                                    'currency': 'inr',
                                    'product_data': {
                                        'name': 'pay',
                                        "metadata": serializers.data,
                                    },
                                    'unit_amount': int(amount_pay) * 100,
                                },
                                'quantity': 1,
                            }],
                            mode='payment',
                            success_url=f'{os.environ.get("url")}/api/resident/payment-success/',
                            cancel_url=f'{os.environ.get("url")}/api/resident/payment-cancel/',
                        )
                        card_obj = stripe.PaymentMethod.create(
                            type="card",
                            card={
                                "number": "4242424242424242",
                                "exp_month": 7,
                                "exp_year": 2023,
                                "cvc": "314",
                            },
                        )
                        customer = stripe.Customer.create(
                            email=request.user.email, payment_method=card_obj.id
                        )

                        return JsonResponse({'id': session})
                return Response({'status':0, 'msg': AlreadyPaid}, status=status.HTTP_400_BAD_REQUEST)
        except UserRole.DoesNotExist:
            return Response({'status': 'fail', 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionPayMaintance(APIView):
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
        try:
            user_role = UserRole.objects.get(user=current_user)
            if user_role:
                currentMonth = datetime.now().month
                currentYear = datetime.now().year
                user_house = user_role.house_no
                data['house_no'] = user_house
                data['is_complete_pay'] = True
                # amount_mqintenance = AmountPayMaintenance.objects.all().only("amount_pay").first()
                amount_mqintenance = 2560
                # amount_pay = int(amount_mqintenance.amount_pay)
                amount_pay = int(amount_mqintenance)
                data['amount_pay']= amount_pay
                print(f"Only pay:- {amount_pay}")
                queryset = UserPayMaintenance.objects.filter(house_no=user_house, pay_date__month=currentMonth,
                                                             pay_date__year=currentYear).first()
                if queryset is None:
                    serializers = UserPayMaintenanceSerializers(data=data)
                    print(f"serial {serializers}")
                    if serializers.is_valid(raise_exception=True):
                        customer = stripe.Customer.create(
                            email=request.user.email
                        ),
                        session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            mode="subscription",
                            line_items=[{
                                'price_data': {
                                    'currency': 'inr',
                                    'recurring':{"interval": "month"},
                                    'product_data': {
                                        'name': 'pay',
                                        "metadata": serializers.data,
                                    },
                                    'unit_amount': int(amount_pay) * 100,
                                },
                                'quantity': 1,

                            }],
                            success_url=f'{os.environ.get("url")}/api/resident/payment-success/',
                            cancel_url=f'{os.environ.get("url")}/api/resident/payment-cancel/',
                        )
                        card_obj = stripe.PaymentMethod.create(
                            type="card",
                            card={
                                "number": "4242424242424242",
                                "exp_month": 7,
                                "exp_year": 2023,
                                "cvc": "314",
                            },
                        )

                        return JsonResponse({'id': session})
                return Response({'status': 0, 'msg': AlreadyPaid}, status=status.HTTP_400_BAD_REQUEST)
        except UserRole.DoesNotExist:
            return Response({'status': 0, 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)

def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


endpoint_secret = 'STRIPE_WEBHOOK_SECRET'


# Using Django
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=201)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_intent = stripe.checkout.Session.list(
            payment_intent=session["payment_intent"],
            expand=['data.line_items']
        )
        product_id = payment_intent['data'][0]['line_items']['data'][0]['price']['product']
        product = stripe.Product.retrieve(product_id)
        print(product, "productproductproductproductproductproduct")
        create_order(**product['metadata'])
        print(f"create_order {create_order}")
    print(event['type'])
    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        create_order(**session['metadata'])
    return HttpResponse(status=200)


def create_order(**data):
    serializer = UserPayMaintenanceSerializers(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()


class UserWillRedirectAfterPay(APIView):
    """
    After user will pay through payment gateway.User can hit this api check here payment successfully added into the system
    Request get:
        HTTP.Request
    Response Objects:
        If user had paid the maintenance then it will show him success msg or not paid it will show him error msg
        IF any other role login into the system then error exception handel raise
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        data = request.data.copy()
        try:
            user_role = UserRole.objects.get(user=current_user)
            if user_role:
                currentMonth = datetime.now().month
                currentYear = datetime.now().year
                user_house = user_role.house_no
                queryset = UserPayMaintenance.objects.filter(house_no=user_house, pay_date__month=currentMonth,
                                                             pay_date__year=currentYear).first()
                print(queryset)
                if queryset and queryset.is_complete_pay:
                    print(queryset.is_complete_pay)
                    return Response({'status': 1, 'msg': SuccessfullyPaid}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 0, 'msg':ErrorOccur
                                     }, status=status.HTTP_400_BAD_REQUEST)

        except UserRole.DoesNotExist:
            return Response({'status': 0, 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({'status': 1, 'data': serializer.data}, status=status.HTTP_200_OK)

class AdminUpdateAmountMiantance(APIView):
    """
    Admin of the system can update the maintenance of the system it will go update request into the system
    Request Put:
        Http.Put
        admin need new amount pay into thr system
    Response Objects:
        If amount update success admin will return with success msg or error raise it will show error msg
    """
    permission_classes = [IsAdminUser]
    def put(self,request):
        queryset = AmountPayMaintenance.objects.all().only("amount_pay").first()
        amount_pay = request.data
        serializers = AdminUpdateAmountMiantanceSerializers(queryset, data=amount_pay)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'status': 'pass`', 'msg': AmountUpdate}, status=status.HTTP_200_OK)
        return Response({'status': 0, 'msg': AlreadyPaid}, status=status.HTTP_400_BAD_REQUEST)



