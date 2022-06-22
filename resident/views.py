""" Importing Libraries """
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserListSerializer
from .models import UserRole
from .message import UserNotGiven, UserStatus, UserAlreadyVerified

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



