from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('accumulate/', views.accumulatePointByUserId),
    path('checkbalance/',views.getUserBalance),
    path('listhistory/', views.listPointHistories),
    path('redeem/', views.redeemPointByUserId)
]