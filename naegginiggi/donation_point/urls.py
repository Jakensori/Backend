from django.urls import path
from . import views

urlpatterns = [
    path('fail/',views.approve),
    path('approve/',views.approve),
    path('cancel/',views.approve),
    path('kakaopay/', views.index),
    path('approval/', views.approval),
    path('accumulate/', views.accumulatePointByUserId),
    path('checkbalance/',views.getUserBalance),
    path('listhistory/', views.listPointHistories),
    path('redeem/', views.redeemPointByUserId),
]