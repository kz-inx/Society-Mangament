""" Importing Libraries """
from django.urls import path, include
from .views import AdminSentNotifcationParticular,SeeVisitors

""" End points where the perform the operation into the system """
urlpatterns = [
    path('see-user/', AdminSentNotifcationParticular.as_view()),
    path('see-visitors/',SeeVisitors.as_view()),
]