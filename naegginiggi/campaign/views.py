from django.shortcuts import render
from campaign.models import Campaign, Review, User_Campaign
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from rest_framework import status
from datetime import datetime
from .serializers import CampaignSerializer,ReviewSerializer
from user.models import User
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
# Create your views here.

## 비동기 실시간 챗 구현

def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user
        
    user = get_object_or_404(User,user=user)
    campaign=Campaign.objects.get(id=room_name)
    user_campaign = get_object_or_404(User_Campaign, user=user, campaign=campaign)
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name
    })
    
    
@api_view(['POST'])
def updateCampaign(request):
    with open('naegginiggi/result.json','r') as file:
        data = json.load(file)
    datetime_format = "%Y%m%d"   
    
    for i in range(len(data)):
        temp = data[i]
        Campaign.objects.create(
            rdonaBoxNo = temp['rdonaBoxNo'],
            title = temp['title'],
            image = temp['defaultImage'],
            summary = temp['summary'],
            hlogName = temp['hlogName'],
            startYmd = datetime.strptime(temp['startYmd'],datetime_format),
            endYmd = datetime.strptime(temp['endYmd'],datetime_format),
            currentAmount = temp['currentAmount'],
            donationCount = temp['donationCount'],
            goalAmount = temp['goalAmount']
        )
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def loadCampaign(request):
    campaign=Campaign.objects.all()
    campaignserializer = CampaignSerializer(campaign, many=True).data
    return Response(campaignserializer, status=status.HTTP_200_OK)


@api_view(['GET'])
def campaignOne(request,campaign_id):
    campaign=Campaign.objects.get(campaign_id=campaign_id)
    campaignserializer = CampaignSerializer(campaign).data  
    # 기부 참여자 불러오기
    user_campaign=User_Campaign.objects.filter(campaign=campaign)
    users=[]
    for i in user_campaign:
        users.append(i.user.username)
    return Response({"campaign_info":campaignserializer, "donator":users}, status=status.HTTP_200_OK)


@api_view(['POST'])
def updateReview(request, campaign_id):
    campaign=Campaign.objects.get(campaign_id=campaign_id)
    title=request.data['title']
    content=request.data['content']
    Review.objects.create(
        campaign=campaign,
        title=title,
        content=content
    )
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def loadReview(request,campaign_id):
    campaign=Campaign.objects.get(campaign_id=campaign_id)
    review=Review.objects.filter(campaign=campaign)
    reviewserializer = ReviewSerializer(review).data    
    return Response(reviewserializer, status=status.HTTP_200_OK)


@api_view(['GET'])
def mydonations(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user

    user = get_object_or_404(User,user=user)
    user_campaign=User_Campaign.objects.filter(user=user)
    result_list=[]
    for i in user_campaign:
        campaign=i.campaign
        campaign=Campaign.objects.get(id=campaign.id)
        campaignserializer = CampaignSerializer(campaign).data
        campaignserializer['mydonation_amount'] = i.donation_amount
        result_list.append(campaignserializer)
    return Response(result_list, status=status.HTTP_200_OK)