from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from knox.auth import TokenAuthentication

from user_custom.models import User_Custom
from campaign.models import User_Campaign, Campaign
# Create your views here.
def define_user(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    token = str(token).split()[1].encode("utf-8")
    knoxAuth = TokenAuthentication()
    user, auth_token = knoxAuth.authenticate_credentials(token)
    return user


def approve(request):
    render('approve.html')
    
    
# 유저, 기부금액, 캠페인아이디 필요
@api_view(['POST'])
def index(request):
    user = define_user(request)
    campaign = get_object_or_404(Campaign, campaign_id=request.data['campaign_id'])
    donation = request.data['donation']
    URL = 'https://kapi.kakao.com/v1/payment/ready'
    headers = {
        "Authorization": "KakaoAK " + "d67108a72dca85785839d343f6075928",   # 변경불가
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "partner_order_id": str(campaign.campaign_id),     # 주문번호
        "partner_user_id": str(user.username),    # 유저 아이디
        "item_name": str(campaign.title),        # 구매 물품 이름
        "quantity": "1",                # 구매 물품 수량
        "total_amount": str(donation),        # 구매 물품 가격
        "tax_free_amount": "0",         # 구매 물품 비과세
        "approval_url": "http://127.0.0.1:8000/donation/approve/",
        "cancel_url": "http://127.0.0.1:8000/donation/cancel/",
        "fail_url": "http://127.0.0.1:8000/donation/fail/",
    }

    res = requests.post(URL, headers=headers, params=params)
    # 결제 승인시 사용할 tid를 세션에 저장
    # next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
    
    return Response(res,status=status.HTTP_200_OK)


@api_view(['POST'])
def approval(request):
    user = define_user(request)
    campaign = get_object_or_404(Campaign, id=request.data['campaign_id'])
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "d67108a72dca85785839d343f6075928",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.data['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": str(campaign.campaign_id),     # 주문번호
        "partner_user_id": str(user.username),    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    return Response(context, status=status.HTTP_200_OK)


# 카카오 페이 결재 완료된 후에 캠페인 아이디랑 결제한 포인트 넘겨주기 !!

@api_view(['POST'])
def accumulatePointByUserId(request):
    user = define_user(request)
    url = "https://api.luniverse.io/svc/v2/mercury/point/save"
    point_amount = request.data['point']
    campaign_id = request.data['campaign_id']
    campaign = get_object_or_404(User_Campaign, id=campaign_id)
    user_custom = get_object_or_404(User_Custom, user=user)
    description = str(timezone.now()) + " " + \
        str(user.username)+" " + str(point_amount) + " 포인트 충전"
    if User_Campaign.objects.filter(user=user, campaign=campaign).exists():
        User_Campaign.objects.get(
            user=user, campaign=campaign).donation_amount += point_amount
    else:
        User_Campaign.objects.create(
            user=user,
            campaign=campaign,
            donation_amount=point_amount
        )
    payload = {
        "orderIdentifier": str(user.username)+"USER_add "+str(user_custom.donation_count+1)+"to Campaign "+str(campaign_id),
        "userIdentifier": str(user.password),
        "loyaltyProgramId": "1564707676167177217",
        "amount": str(point_amount),
        "description": description,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.post(url, json=payload, headers=headers)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def redeemPointByUserId(request):
    user = define_user(request)
    url = "https://api.luniverse.io/svc/v2/mercury/point/spend"
    point_amount = request.data['point']
    user_custom = get_object_or_404(User_Custom, user=user)
    campaign_id = request.data['campaign_id']
    campaign = get_object_or_404(User_Campaign, id=campaign_id)
    User_Campaign.objects.get(
        user=user, campaign=campaign).donation_amount -= point_amount

    payload = {
        "orderIdentifier": str(user.username)+"USER_redeem "+str(user_custom.donation_count+1)+"to Campaign "+str(campaign_id),
        "userIdentifier": str(user.password),
        "loyaltyProgramId": "1564707676167177217",
        "amount": str(point_amount),
        "description": str(timezone.now()) + " " + str(user.username)+" " + str(point_amount) + " 포인트 차감"
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }

    response = requests.post(url, json=payload, headers=headers)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def getUserBalance(request):
    user = define_user(request)
    url = "https://api.luniverse.io/svc/v2/mercury/point-accounts/" + \
        str(user.password)+"/balances/MEAL"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.get(url, headers=headers)
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def listPointHistories(request):
    user = define_user(request)
    url = "https://api.luniverse.io/svc/v2/mercury/point/histories?userIdentifier=" + \
        str(user.password)+"&loyaltyProgramId=1564707676167177217&rpp=50&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.get(url, headers=headers)
    return Response(response, status=status.HTTP_200_OK)
