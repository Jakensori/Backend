from django.urls import path
from . import views

urlpatterns = [
    path('', views.todayrecord),
    path('upload/', views.addrecord),
    path('settlement/', views.todaysettlement),
]