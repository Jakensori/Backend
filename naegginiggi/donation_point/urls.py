from django.urls import path
from . import views

urlpatterns = [
    path('fail/',views.fail),
    path('request/', views.payments_request),
    path('approve/', views.payments_approve),
    path('info/', views.get_account_info),
    path('cancel/', views.cancel_payments),
    path('accumulate/', views.accumulatePointByUserId),
    path('listhistory/', views.listPointHistories),
    path('redeem/', views.redeemPointByUserId),
    path('receipt/', views.donation_receipt),
]
