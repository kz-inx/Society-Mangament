from django.urls import path, include
from user.views import UserRegistrationView, LoginIntoSystem, StaffRegistrationView, \
    UserChangePasswordView, PasswordResetView, PasswordResetConfirm
urlpatterns = [
    path('register-user/', UserRegistrationView.as_view()),
    path('register-staff/', StaffRegistrationView.as_view()),
    path('login/', LoginIntoSystem.as_view()),
    path('change-password/', UserChangePasswordView.as_view()),
    path('password_reset/',PasswordResetView.as_view()),
    path('Password-reset/confirm/', PasswordResetConfirm.as_view())


]