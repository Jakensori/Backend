from django.shortcuts import render
from campaign.models import Campaign
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from rest_framework import status
from datetime import datetime
# Create your views here.

## 비동기 실시간 챗 구현

def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
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
        campaign = Campaign.objects.create(
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