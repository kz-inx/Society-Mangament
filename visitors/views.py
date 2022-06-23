""" Importing Libraries """
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from staffresident.models import StaffRole
from .serializers import VisitorsRegisterSerializers, SeeVisitorsSerializers
from .models import VisitorsSociety
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from user.models import User
from resident.models import UserRole
from .message import VerfiyVistiors, NotStaff, NotUser, VistiorsNotAvailable, VisitorsStatus, VisitorIsAllAlreadyVerfied

""" creating a apiview to sent the notifcation to the user which visitors has come to meet him """
class AdminSentNotifcationParticular(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        current_user = request.user

        try:
            staff_role = StaffRole.objects.get(user=current_user)
            serializer = VisitorsRegisterSerializers(data=request.data, context={'request':self.request})
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
                    'djangoblogkunal@gmail.com',
                    email_list,
                    fail_silently=False,
                )
                return Response({'status':'Successfully','msg':VerfiyVistiors}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except StaffRole.DoesNotExist:
            return Response({'status':'fail','msg':NotStaff}, status=status.HTTP_400_BAD_REQUEST)


""" creating a endpoint where user come see which visitors has come meet him"""
class SeeVisitors(ListAPIView):
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
            print(e,type(e))
            return Response({'status': 'fail', 'msg':NotUser},status=status.HTTP_400_BAD_REQUEST)


"creating a class will visitors will verify or reject the visitors and staff will notify via email "
class UpdateStatusVisitors(APIView):
    permission_classes = [IsAuthenticated]

    def post (self,request):
        current_user = request.user
        print(f"Current user is:- {current_user}")
        # print(request.user.id)
        try:
            staff_role = UserRole.objects.get(user=current_user)
            if staff_role:
                visitor_id = request.data.get('id')
                visitor_id= get_object_or_404(VisitorsSociety,id=visitor_id)
                visitor_status = request.data.get('is_status')
                user_id = request.user.user_data.get()
                visitor = VisitorsSociety.objects.get(id=visitor_id)
                visitor.is_status=visitor_status
                visitor.user = user_id
                if not visitor.is_answer:

                    visitor.is_answer=True
                    visitor.save()
                    staff = visitor.staff
                    staff_email = staff.user.email
                    send_mail(
                        'Status Update Related Visitors',
                        visitor_status,
                        'djangoblogkunal@gmail.com',
                        [staff_email],
                        fail_silently=False,
                    )
                    if visitor is None:
                        return Response({'status':'Not available','msg':VistiorsNotAvailable},status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({'status':'Solved','msg':VisitorsStatus}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'Not available', 'msg': VisitorIsAllAlreadyVerfied },
                                    status=status.HTTP_404_NOT_FOUND)

        except UserRole.DoesNotExist:
            return Response({'status':'fail','msg':NotUser},status=status.HTTP_400_BAD_REQUEST)





