from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.serializers import UserRegistrationSerializer, UserLoginSerializer, UserChangePasswordSerializer, UserProfileSerializer
from resident.serializers import UserDataEnter
from staffresident.serializers import StaffData
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from resident.models import UserRole
from staffresident.models import StaffRole
from .message import UserRegstration, UserWrong, UserEmailNotMatch, UserNotVerified, UserLogin, UserChangepassword, \
    PasswordResetConform, PasswordResetLinkSent, StaffChangePassword, StaffChangePasswordAnother

""" Generating the token for the system """


def get_tokens_for_user(user):
    print(user, "user")
    # print(user.user_id,"user_id")
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


""" Creating a class view for regstration to the new user into our system"""


class UserRegistrationView(APIView):

    def post(self, request, fromat=None):
        commonserializer = UserRegistrationSerializer(data=request.data.get("commondata"))
        if commonserializer.is_valid(raise_exception=True):
            user = commonserializer.save()
            request.data['user'] = user
            userserializer = UserDataEnter(data=request.data.get("userdata"))
            if userserializer.is_valid(raise_exception=True):
                user = userserializer.save(user=user)
                token = get_tokens_for_user(user)
                return Response(
                    {'Status': "Okk", 'access': token['access'], 'refresh': token['refresh'], 'msg': UserRegstration},
                    status=status.HTTP_201_CREATED)
            return Response({'Status': "Fail", "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Status': "Fail", "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)


""" Creating a class view for regstration to the new staff role into your system...."""


class StaffRegistrationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, fromat=None):
        commonserializer = UserRegistrationSerializer(data=request.data.get("commondata"))
        if commonserializer.is_valid(raise_exception=True):
            user = commonserializer.save()
            request.data['user'] = user
            staffserializer = StaffData(data=request.data.get("staffdata"))
            if staffserializer.is_valid(raise_exception=True):
                user = staffserializer.save(user=user)
                token = get_tokens_for_user(user)
                return Response(
                    {'Status': "Okk", 'access': token['access'], 'refresh': token['refresh'], 'msg': UserRegstration},
                    status=status.HTTP_201_CREATED)
            return Response({'Status': "Fail", "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Status': "Fail", "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)


""" Creating a class view for login into the system..."""


class LoginIntoSystem(APIView):

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user_auth = authenticate(email=email, password=password)
        print(user_auth, "authenticated")
        user = UserRole.objects.filter(is_verfied=False, user=user_auth).first()
        # print(user.house_no)
        print(user, "detailed")
        # print(user,"")
        if user_auth is None:
            return Response({'msg': UserEmailNotMatch}, status=status.HTTP_404_NOT_FOUND)
        elif user:
            return Response({'msg': UserNotVerified}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = get_tokens_for_user(user_auth)
            return Response({'access': token['access'], 'refresh': token['refresh'], 'msg': UserLogin},
                            status=status.HTTP_200_OK)


""" User change password by providing the necessary details"""
class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        current_user = request.user
        print(current_user)
        try:
            staff_role = StaffRole.objects.get(user=current_user)
            if staff_role:
                serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
                serializer.is_valid(raise_exception=True)
                if not staff_role.change_password:
                    staff_role.change_password = True
                    staff_role.save()
                    return Response({'msg': StaffChangePassword}, status=status.HTTP_200_OK)

                return Response({'msg': StaffChangePasswordAnother}, status=status.HTTP_200_OK)

        except StaffRole.DoesNotExist:
            serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            return Response({'msg': UserChangepassword}, status=status.HTTP_200_OK)


"""Overriding post method for changing Response"""


class PasswordResetView(ResetPasswordRequestToken):

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetView, self).post(request)
        return Response(
            {'status': 'OK', 'message': PasswordResetLinkSent},
            status=response.status_code
        )


"""Overriding post method for changing Response"""
class PasswordResetConfirm(ResetPasswordConfirm):

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetConfirm, self).post(request)
        return Response(
            {'status': 'OK', 'message': PasswordResetConform},
            status=response.status_code
        )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
