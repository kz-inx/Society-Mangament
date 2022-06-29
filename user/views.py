from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordConfirm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView, ListAPIView, get_object_or_404
from user.serializers import UserRegistrationSerializer, UserLoginSerializer, UserChangePasswordSerializer,AdminDeleteUserSerializers
from resident.serializers import UserDataEnter, GetUserData, UserViewProfile
from staffresident.serializers import StaffData, GetStaffData, StaffViewProfile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from resident.models import UserRole
from staffresident.models import StaffRole
from .message import UserRegstration, UserWrong, UserEmailNotMatch, UserNotVerified, UserLogin, UserChangepassword, \
    PasswordResetConform, PasswordResetLinkSent, StaffChangePassword, StaffChangePasswordAnother, UserNotAvailable, \
    UserAlreadyBlock, UserBlock, BlockUser, DeleteUserStaff

""" Generating the token for the system """
def get_tokens_for_user(user):
    print(user, "user")
    # print(user.user_id,"user_id")
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    """
    Creating a class view for regstration to the new user into our system
    """
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

class StaffRegistrationView(APIView):
    """
    Creating a class view for regstration to the new staff role into your system....
    """
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

class LoginIntoSystem(APIView):
    """
    Creating a class view for login into the system...
    """
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user_auth = authenticate(email=email, password=password)
        print(user_auth, "authenticated")
        if not user_auth:
            return Response({'status': 'fail', 'msg': UserEmailNotMatch}, status=status.HTTP_404_NOT_FOUND)
        try:
            user_auth.staffrole_set.get()
            token = get_tokens_for_user(user_auth)
            return Response(
                {'status': 'okk', 'access': token['access'], 'refresh': token['refresh'], 'msg': UserLogin},
                status=status.HTTP_200_OK)
        except:
            print("Not staff")

        user_verified = user_auth.user_data.get()
        if not user_verified.is_verfied:
            return Response({'status': 'Unverified', 'msg': UserNotVerified}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = get_tokens_for_user(user_auth)
            return Response(
                {'status': 'okk', 'access': token['access'], 'refresh': token['refresh'], 'msg': UserLogin},
                status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    """
    User change password by providing the necessary details
    """
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

class PasswordResetView(ResetPasswordRequestToken):
    """
    Overriding post method for changing Response
    """
    def post(self, request, *args, **kwargs):
        response = super(PasswordResetView, self).post(request)
        return Response(
            {'status': 'OK', 'message': PasswordResetLinkSent},
            status=response.status_code
        )

class PasswordResetConfirm(ResetPasswordConfirm):
    """
    Overriding post method for changing Response
    """

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetConfirm, self).post(request)
        return Response(
            {'status': 'OK', 'message': PasswordResetConform},
            status=response.status_code
        )

class UserProfileView(APIView):
    """
    User can see his profile in the system...
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        try:
            staff_role = StaffRole.objects.get(user=current_user)
            if staff_role:
                serializer = StaffViewProfile(staff_role)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except StaffRole.DoesNotExist:
            resident_user = UserRole.objects.get(user=current_user)
            if resident_user:
                serializer = UserViewProfile(resident_user)
                return Response(serializer.data, status=status.HTTP_200_OK)

class AdminBlockUser(APIView):
    permission_classes = [IsAdminUser]
    """
    Block the user or staff in the system
    """
    def post(self,request):
        user_id = request.data.get('id')
        # user_id = get_object_or_404(User, id=user_id)
        user_block = User.objects.filter(id=user_id).first()
        if user_block is None:
            return Response({'status':'Fail','msg':UserNotAvailable},status=status.HTTP_400_BAD_REQUEST)
        elif not user_block.is_active:
            return Response({'status':'Fail','msg':UserAlreadyBlock}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_block.is_active = False
            user_block.save()
            return Response({'status':'Pass','msg':UserBlock},status=status.HTTP_200_OK)

class AdminDeleteUser(DestroyAPIView):
    """
    Admin will delte the user perament from the
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminDeleteUserSerializers
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        response = super(AdminDeleteUser, self).delete(request, *args, **kwargs)
        return Response({
            'status':'Pass',
            'msg':DeleteUserStaff
        }, status=response.status_code)

class AdminSeeAllStaff(ListAPIView):
    """
    Admin Will see all details of the staff register into the system
    """
    permission_classes = [IsAdminUser]
    queryset = StaffRole.objects.all()
    serializer_class = GetStaffData

class AdminSeeAllUser(ListAPIView):
    """
    Admin Will see all details of the user register into the system
    """
    permission_classes = [IsAdminUser]
    queryset = UserRole.objects.all()
    serializer_class = GetUserData

