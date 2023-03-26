from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.todayrecord),
    path('upload/', views.addrecord),
    path('settlement/<int:user_id>/', views.todaysettlement),
    path('accountbook/', views.month_accountbook),
    path('category/<int:user_id>/', views.category_analysis),
    path('time/<int:user_id>/', views.time_analysis),
]