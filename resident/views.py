""" Importing Libraries """
import datetime as DT
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserListSerializer,UserPayMaintenanceSerializers
from .models import UserRole
from .message import UserNotGiven, UserStatus, UserAlreadyVerified, SuccessfullyPaid, ErrorOccur, AlreadyPaid, NotUser
from .models import UserPayMaintenance

""" Admin will see user whose status is_verified is false """
class UserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserRole.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        queryset = UserRole.objects.filter(is_verfied=False)
        return queryset


""" Admin will update the status and give the permission to the user access the application """
class UserStatusUpdate(APIView):
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
    permission_classes = [IsAuthenticated]
    query_set = UserPayMaintenance.objects.all()
    def post(self,request):
        current_user = request.user
        data = request.data.copy()
        try:
            user_role = UserRole.objects.get(user=current_user)
            print(f"User Role:- {user_role}")
            if user_role:
                today = DT.date.today()
                month_ago = today + DT.timedelta(days=30)
                user_house = user_role.house_no
                data['next_pay_date'] = month_ago
                data['house_no'] = user_house
                queryset = UserPayMaintenance.objects.filter(house_no=user_house , next_pay_date__lt=today).first()
                if queryset:
                    print(queryset)
                    serializers= UserPayMaintenanceSerializers(data=data)
                    if serializers.is_valid(raise_exception=True):
                        serializers.save()
                        return Response({'status': 'pass', 'msg': SuccessfullyPaid}, status=status.HTTP_200_OK)
                    return Response({'status': 'fail', 'msg': ErrorOccur}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'status': 'fail', 'msg': AlreadyPaid},status=status.HTTP_400_BAD_REQUEST)

        except UserRole.DoesNotExist:
            return Response({'status': 'fail', 'msg': NotUser}, status=status.HTTP_400_BAD_REQUEST)









