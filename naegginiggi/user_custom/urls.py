from django.urls import path
from . import views

urlpatterns = [
    path('', views.monthBudget),
    path('mydonation/', views.donation_box),
    path('mypage/', views.mypageUser),
    path('budget/', views.patch_budget),
    path('mealpoint/<int:user_id>/', views.mealpoint),
    path('savings/', views.savings_amount),
]
