from django.urls import path
from . import views

urlpatterns = [
    path('', views.monthBudget),
    path('mydonation/', views.donation_box),
    path('mypage/', views.mypageUser),
]