""" Importing libraries """
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
    UserAlreadyBlock, UserBlock, DeleteUserStaff, NewAdminSystem, UserAlreadyBlockORAdmin

""" Generating the token for the system """
def get_tokens_for_user(user):
    print(user, "user")
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    """
    Creating a class view for regstration to the new user into our system
       Accepts the post request into the system
    Request:
        Http Request will there
        it will contain all the data required in the model and stored into database
    Returns:
            Request.objects
            if all value are corrected new account will create of user show success msg in the form of json format
            if anything goes wrong system throw the error in the form of json
    """
    def post(self, request, fromat=None):
        commonserializer = UserRegistrationSerializer(data=request.data)
        if commonserializer.is_valid(raise_exception=True):
            user = commonserializer.save()
            data = request.data.copy()
            data['user'] = user
            userserializer = UserDataEnter(data=data)
            if userserializer.is_valid(raise_exception=True):
                user = userserializer.save(user=user)
                token = get_tokens_for_user(user)
                print(token)
                return Response(
                    {'Status': 1, 'access': token['access'], 'refresh': token['refresh'], 'msg': UserRegstration},
                    status=status.HTTP_201_CREATED)
            return Response({'Status': 0, "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Status': 0, "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)

class StaffRegistrationView(APIView):
    """
    Creating a class view for regstration to the new staff role into your system....
    there only admin of the system has permission to perform this operation into the system
    Accepted the post request into the system
    Request:
        Http Request will there
        it will contain all the data required in the model and stored into the database into the system
    Returns:
            Request. Objects
            if all value are corrected new account will create of staff show success msg in format json
            if anything goes wrong system throw the error and going failure msg in the format json
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
                    {'Status': 1, 'access': token['access'], 'refresh': token['refresh'], 'msg': UserRegstration},
                    status=status.HTTP_201_CREATED)
            return Response({'Status': 0, "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Status': 0, "msg": UserWrong}, status=status.HTTP_400_BAD_REQUEST)

class LoginIntoSystem(APIView):
    """
    Creating a class view for login into the system..
    User need provide credentials for login into the system

    Request:
        Http Request will there
        it will contain all the data required in the model. They need to enter email id and password
    Return:
        Request. Object
        it will request by the client
        it will check user is verified form admin or not. If not it will throw the error
        or else
        it will generate token and login into the system successfully
    """
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user_auth = authenticate(email=email, password=password)
        print(user_auth, "authenticated")
        if not user_auth:
            return Response({'status': 0, 'msg': UserEmailNotMatch}, status=status.HTTP_404_NOT_FOUND)
        try:
            user_auth.staffrole_set.get()
            token = get_tokens_for_user(user_auth)
            return Response(
                {'status': 1, 'access': token['access'], 'refresh': token['refresh'], 'msg': UserLogin},
                status=status.HTTP_200_OK)
        except:
            print("Not staff")

        user_verified = user_auth.user_data.get()
        if not user_verified.is_verfied:
            return Response({'status': 0, 'msg': UserNotVerified}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = get_tokens_for_user(user_auth)
            return Response(
                {'status': 1, 'access': token['access'], 'refresh': token['refresh'], 'msg': UserLogin},
                status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    """
    User change password by providing the necessary details
     client should be verified with his credentials use this feature
    Request Post:
        Http.Request
        User need login to perform this action and enter data need
    Return:
        return.object
        the user password will  be change into the system based on role is classified into the system is staff or user
        if user it will show success msg in the form of the json data,
        if its staff going to check its first time or not, its first time it will true status of change password and
        show success msg in the form of the json data.
        Or else It will raise error and show in the form of json data.
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
                    return Response({'status': 1,'msg': StaffChangePassword}, status=status.HTTP_200_OK)

                return Response({'status': 1,'msg': StaffChangePasswordAnother}, status=status.HTTP_200_OK)

        except StaffRole.DoesNotExist:
            serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            return Response({'status': 1,'msg': UserChangepassword}, status=status.HTTP_200_OK)

class PasswordResetView(ResetPasswordRequestToken):
    """
    Overriding post method for changing Response

    Request Post:
        Http Request
        *args Variable length argument list.
        **kwargs Arbitrary keyword arguments.
        it will send mail for reset password link
    """
    def post(self, request, *args, **kwargs):
        response = super(PasswordResetView, self).post(request)
        return Response(
            {'status': 1, 'message': PasswordResetLinkSent},
            status=response.status_code
        )

class PasswordResetConfirm(ResetPasswordConfirm):
    """
    Overriding post method for changing Response
    Request Post:
        Http Request
        *args Variable length argument list.
        **kwargs Arbitrary keyword arguments.
        it will take the token and new password and it will update into the system
    """

    def post(self, request, *args, **kwargs):
        response = super(PasswordResetConfirm, self).post(request)
        return Response(
            {'status': 1, 'message': PasswordResetConform},
            status=response.status_code
        )

class UserProfileView(APIView):
    """
    the user of the system will be able to see his whole profile into the system
     client need to be authenticated into the system

    Request Get:
        Http.Request
        It will classify based on user login it show profile its staff or its user
    Return:
        Return.objects
        it will return the whole profile information about the users into the system
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
    """
    Block the user or staff in the system
    only admin of the system can perform this operation no-one else has right performed  this operation, or it will raise error
    Request Post:
        HTTP.Request
        Admin need block user id and enter into the format of json data
    Response:
        Response.objects:
        if user is found it will block the user show success msg to the user in form the json data
        if user is already blocked or user is admin of the system then it will show error msg in the form of json data
    """
    permission_classes = [IsAdminUser]
    def post(self,request):
        user_id = request.data.get('id')
        user_block = User.objects.filter(id=user_id).first()
        if not user_block:
            return Response({'status':0,'msg':UserNotAvailable},status=status.HTTP_400_BAD_REQUEST)
        elif not user_block.is_active:
            return Response({'status':0,'msg':UserAlreadyBlock}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_block.is_active = False
            user_block.save()
            return Response({'status':1,'msg':UserBlock},status=status.HTTP_200_OK)

class NewAdminInSystem (APIView):
    # permission_classes = [IsAdminUser]
    """
    Create the new admin into the system 
    only admin of the system has permission to do this or any one else try do this it will raise error msg 
    Request post:
        HTTP.Request
        client need enter the user_id for given admin rights to other user 
    Response Objects:
        If id is true admin access will given and show success msg in the form json data 
        if is already admin or user block into the system it will going to raise the error msg into the system
    """
    def post(self,request):
        user_id = request.data.get('id')
        # user_id = get_object_or_404(User, id=user_id)
        user_block = User.objects.filter(id=user_id).first()
        if not user_block:
            return Response({'status': 0, 'msg': UserNotAvailable},status=status.HTTP_400_BAD_REQUEST)
        elif user_block.is_active and user_block.is_admin:
            return Response({'status':0,'msg':UserAlreadyBlockORAdmin}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_block.is_admin = True
            user_block.save()
            return Response({'status': 1, 'msg': NewAdminSystem},status=status.HTTP_200_OK)

class AdminDeleteUser(DestroyAPIView):
    """
    Admin will delete the user permanent from the
    only admin of the system has right to perform this opeartion or anyone else try to this it will show error msg into the system.
    Request Delete:
        Http.Request
        admin needs user_id for delete user from the system permanently
    Response Objects:
        It will show the success msg after delete user into the system
        if user id not get or user is admin of the system is not able to delete it and raise error msg into the form json
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
    only admin can access this endpoint or any else try do this it will raise the error msg
    It will go to show all staff register details into the system and there necessary information
    """
    permission_classes = [IsAdminUser]
    queryset = StaffRole.objects.all()
    serializer_class = GetStaffData

class AdminSeeAllUser(ListAPIView):
    """
    Admin Will see all details of the user register into the system
    only admin can access this endpoint or any else try do this it will raise the error msg
    It will go to show all user register details into the system and there necessary information
    """
    permission_classes = [IsAdminUser]
    queryset = UserRole.objects.all()
    serializer_class = GetUserData

