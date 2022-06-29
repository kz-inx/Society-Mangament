""" Importing Libraries """
from django.urls import path, include
from .views import AdminSentNotifcationParticular,SeeVisitors, UpdateStatusVisitors,StaffSeeAllVisitors, UserSeeAllVisitors

""" End points where the perform the operation into the system """
urlpatterns = [
    path('register-user/', AdminSentNotifcationParticular.as_view()),
    path('see-visitors/',SeeVisitors.as_view()),
    path('update-status/',UpdateStatusVisitors.as_view()),
    path('staff-see-visitors/',StaffSeeAllVisitors.as_view()),
    path('user-see-visitors/',UserSeeAllVisitors.as_view()),
]