from django.urls import path, include
from user.views import UserRegistrationView, LoginIntoSystem, StaffRegistrationView, \
    UserChangePasswordView, PasswordResetView, PasswordResetConfirm, UserProfileView, AdminBlockUser, \
    AdminSeeAllStaff,AdminSeeAllUser,AdminDeleteUser,NewAdminInSystem
urlpatterns = [
    path('register-user/', UserRegistrationView.as_view(), name='user-register'),
    path('register-staff/', StaffRegistrationView.as_view(), name='staff-register'),
    path('login/', LoginIntoSystem.as_view(), name='login-user'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('password_reset/',PasswordResetView.as_view(), name='password-reset'),
    path('Password-reset/confirm/', PasswordResetConfirm.as_view(), name='password-conformation'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('block-user/', AdminBlockUser.as_view(), name='block-user'),
    path('staff-records/', AdminSeeAllStaff.as_view(), name='staff-records'),
    path('user-records/', AdminSeeAllUser.as_view(), name='user-records'),
    path('delete-user/<int:pk>/',AdminDeleteUser.as_view(), name='delete-user'),
    path('new-admin-system/',NewAdminInSystem.as_view(), name='new-admin')


]