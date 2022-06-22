""" Importing Libraries """
from django.urls import path, include
from .views import RoleRegistrationView

""" creating the endpoint for run the application.... """
urlpatterns = [
    path('register-role/', RoleRegistrationView.as_view()),

]