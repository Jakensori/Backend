from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='chatroom'),
    path('post/update/', views.updateCampaign),  
    path('posts/all/', views.loadCampaign),
    path('posts/<int:campaign_id>/', views.campaignOne),
    path('mydonation/all/', views.mydonations),
    path('user/notification/', views.usernotification),
]
