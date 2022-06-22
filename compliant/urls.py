""" Importing the libraries """
from django.urls import path
from .views import UserFileCompliant,SeeCompliantViews, AdminUpdateStatusCompliant

""" Url patterns for redirect and perform the particular operation in the our system """
urlpatterns = [
    path('compliant/', UserFileCompliant.as_view()),
    path('see-compliant/', SeeCompliantViews.as_view()),
    path('status-update/', AdminUpdateStatusCompliant.as_view())


]