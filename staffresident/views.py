""" Importing Libraries """
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RoleRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from .message import NewRole

class RoleRegistrationView(APIView):
    """
    Admin will different roles in the system
    Only admin of the system is able to access this or any else try it will throw the error
    Request Post:
        Http.Request
        Admin need sent role name which he wants to create in the system
    Return objects:
        If everything is okk then new role will create into the system
        if new role name which exiting role name then it will go throw the error in the form of the json data
     """
    permission_classes = [IsAdminUser]

    def post(self, request, fromat=None):
        serializer = RoleRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            role = serializer.save()
            role.save()
            return Response({"status":1,'msg':NewRole, 'id':role.id }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
