from .models import User_Custom
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from knox.auth import TokenAuthentication
from campaign.models import Campaign
from campaign.serializers import CampaignSerializer

from django.core.paginator import Paginator


# Create your views here.
# 한 달 예산 저장
@api_view(['POST'])
def monthBudget(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user

    user = get_object_or_404(User,user=user)  
    user_custom = User_Custom.objects.create(
        user=user,
        month_budget = request.data['month_budget']
    ) 
    user_custom.save()
    return Response({'data': user_custom.month_budget}, status=status.HTTP_200_OK)


# 한 달 예산 수정
@api_view(['PATCH','GET'])
def patch_budget(request):
    myuser=get_object_or_404(User,id=1)
    user = get_object_or_404(User_Custom, user=myuser)
    if request.method == 'PATCH':
        budget_to_change = request.data['month_budget']
        user.month_budget = budget_to_change
        user.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({"month_budget":user.month_budget},status=status.HTTP_200_OK)

# collection 페이지에서 mealpoint 불러오기
@api_view(['GET'])
def mealpoint(request,user_id):
    user = get_object_or_404(User,id=user_id)
    user_detail = User_Custom.objects.get(user=user)
    return Response({"meal_point":user_detail.donation_temperature, "level":user_detail.donation_count}, status=status.HTTP_200_OK)


# 기부 저금통 누적 금액 불러오기
@api_view(['GET'])
def savings_amount(request):
    user= get_object_or_404(User, id=1)
    user_detail = User_Custom.objects.get(user=user)
    return Response({"savings":user_detail.savings}, status=status.HTTP_200_OK)


# 기부 가능한 캠페인 4개 불러오기
@api_view(['GET'])
def donation_box(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user

    user = get_object_or_404(User,user=user)
    user_detail = User_Custom.objects.get(user=user)
    campaign = Campaign.objects.all()
    paginator = Paginator(campaign, 4).page(1).object_list
    campaignserializer = CampaignSerializer(paginator, many=True).data
    return Response({"total_donation":user_detail.total_donation, "donation_point":user_detail.donation_count, 'page_obj':campaignserializer}, status=status.HTTP_200_OK)


# 마이페이지 유저 정보 불러오기
@api_view(['GET'])
def mypageUser(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user

    myuser = get_object_or_404(User,user=user)
    user_donationtem = User_Custom.objects.get(user=myuser).donation_temperature
    username = myuser.username

    return Response({"username": username, "userid": user.username, "email": user.email, "donation_temperature": user_donationtem}, status=status.HTTP_200_OK)  
