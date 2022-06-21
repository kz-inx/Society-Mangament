from django.urls import path, include
from .views import RoleRegistrationView
urlpatterns = [
    path('register-role/', RoleRegistrationView.as_view()),

]