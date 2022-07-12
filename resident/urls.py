""" Importing Libraries """
from django.urls import path, include
from .views import UserListView, UserStatusUpdate, UserNormalPayMaintance, AdminCanSeeAllRecordsMaintance, \
    success, cancel, stripe_webhook, UserWillRedirectAfterPay, AdminUpdateAmountMiantance,UserSubscriptionPayMaintance

""" End points where the perform the operation into the system """
urlpatterns = [
    path('see-user/', UserListView.as_view()),
    path('user-status/', UserStatusUpdate.as_view()),
    path('user-pay/',UserNormalPayMaintance.as_view()),
    path('user-pay-sub/',UserSubscriptionPayMaintance.as_view()),
    path('admin-see-records/',AdminCanSeeAllRecordsMaintance.as_view()),
    path('payment-success/', success, name='payment-success'),
    path('payment-cancel/',cancel, name='payment-cancel'),
    path('stripe-web/',stripe_webhook, name='stripe_webhook'),
    path('see-after-payment/',UserWillRedirectAfterPay.as_view()),
    path('admin-update-amount/', AdminUpdateAmountMiantance.as_view())
]