""" Importing Libraries """
from django.urls import path, include
from .views import AdminSentNotifcationParticular,SeeVisitors, UpdateStatusVisitors

""" End points where the perform the operation into the system """
urlpatterns = [
    path('register-user/', AdminSentNotifcationParticular.as_view()),
    path('see-visitors/',SeeVisitors.as_view()),
    path('update-status/',UpdateStatusVisitors.as_view()),
]