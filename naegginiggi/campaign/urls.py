from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='chatroom'),
    path('update/', views.updateCampaign),  
    path('posts/all/', views.loadCampaign),
    path('posts/<int:campaign_id>/', views.campaignOne),
]