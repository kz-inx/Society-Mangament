""" Importing libraries """
from django.urls import path, include
from .views import AdminSentNotifcationAll, SeeNotifcation, AdminSentNotifcationParticular

""" creating endpoints where we can go and perform the particular operation with given data"""
urlpatterns = [
    path('sendall/', AdminSentNotifcationAll.as_view()),
    path('sendoneuser/', AdminSentNotifcationParticular.as_view()),
    path('see-notify', SeeNotifcation.as_view())

]