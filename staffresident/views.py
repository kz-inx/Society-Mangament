""" Importing Libraries """
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RoleRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from .message import NewRole

""" Generating tokes for the staff regstration and user login """
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

""" Admin will different roles in the system """
class RoleRegistrationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, fromat=None):
        serializer = RoleRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            role = serializer.save()
            role.save()
            return Response({"status":"Done",'msg':NewRole }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
