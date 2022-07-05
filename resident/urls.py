""" Importing Libraries """
from django.urls import path, include
from .views import UserListView, UserStatusUpdate, UserPayMaintance, AdminCanSeeAllRecordsMaintance

""" End points where the perform the operation into the system """
urlpatterns = [
    path('see-user/', UserListView.as_view()),
    path('user-status/', UserStatusUpdate.as_view()),
    path('user-pay/',UserPayMaintance.as_view()),
    path('admin-see-records/',AdminCanSeeAllRecordsMaintance.as_view())
]