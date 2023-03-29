from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from knox.auth import TokenAuthentication

from user_custom.models import User_Custom
from campaign.models import User_Campaign
# Create your views here.

# def first(request):
#     return render(request, 'kakaopay_redirectPage.html')


# @api_view(['POST'])
# def index(request):
#         URL = 'https://kapi.kakao.com/v1/payment/ready'3
#         headers = {
#             "Authorization": "KakaoAK " + "d67108a72dca85785839d343f6075928",   # 변경불가
#             "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
#         }
#         params = {
#             "cid": "TC0ONETIME",    # 테스트용 코드
#             "partner_order_id": "1001",     # 주문번호
#             "partner_user_id": "admin",    # 유저 아이디
#             "item_name": "기부 포인트 1000 meal 결재",        # 구매 물품 이름
#             "quantity": "1000",                # 구매 물품 수량
#             "total_amount": "1000",        # 구매 물품 가격
#             "tax_free_amount": "0",         # 구매 물품 비과세
#             "approval_url": "http://127.0.0.1:8000/donation/approval/",
#             "cancel_url": "http://127.0.0.1:8000/donation/",
#             "fail_url": "http://127.0.0.1:8000/donation/",
#         }

#         res = requests.post(URL, headers=headers, params=params)
#         request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
#         next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
#         return redirect(next_url)

#     return render('kakaopay_redirectPage.html')


# def approval(request):
#     URL = 'https://kapi.kakao.com/v1/payment/approve'
#     headers = {
#         "Authorization": "KakaoAK " + "자신의 admin key 넣기",
#         "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
#     }
#     params = {
#         "cid": "TC0ONETIME",    # 테스트용 코드
#         "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
#         "partner_order_id": "1001",     # 주문번호
#         "partner_user_id": "german",    # 유저 아이디
#         "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
#     }

#     res = requests.post(URL, headers=headers, params=params)
#     amount = res.json()['amount']['total']
#     res = res.json()
#     context = {
#         'res': res,
#         'amount': amount,
#     }
#     return render(request, 'approval.html', context)
######### 카카오 페이 결재 완료된 후에 캠페인 아이디 넘겨주기 !!


def define_user(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    token = str(token).split()[1].encode("utf-8")
    knoxAuth = TokenAuthentication()
    user, auth_token = knoxAuth.authenticate_credentials(token)
    return user


@api_view(['POST'])
def accumulatePointByUserId(request):
    user = define_user(request)
    url = "https://api.luniverse.io/svc/v2/mercury/point/save"
    point_amount = request.data['point']
    campaign_id = request.data['campaign_id']
    campaign = get_object_or_404(User_Campaign, id=campaign_id)
    user_custom = get_object_or_404(User_Custom, user = user)
    description = str(timezone.now()) + " "+ str(user.username)+" "+ str(point_amount) + " 포인트 충전"
    if User_Campaign.objects.filter(user=user,campaign=campaign).exists():
        User_Campaign.objects.get(user=user, campaign=campaign).donation_amount += point_amount
    else:
        User_Campaign.objects.create(
            user=user,
            campaign=campaign,
            donation_amount = point_amount
        )
    payload = {
        "orderIdentifier" : str(user.username)+"USER_add "+str(user_custom.donation_count+1)+"to Campaign "+str(campaign_id),
        "userIdentifier" : str(user.password),
        "loyaltyProgramId" : "1564707676167177217",
        "amount" : str(point_amount),
        "description" : description,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.post(url, json=payload, headers=headers)
    User_Campaign.objects.create(
        
    )
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def redeemPointByUserId(request):
    user = define_user(request)
    url = "https://api.luniverse.io/svc/v2/mercury/point/spend"
    point_amount = request.data['point']
    user_custom = get_object_or_404(User_Custom, user = user)
    campaign_id = request.data['campaign_id']
    campaign = get_object_or_404(User_Campaign, id=campaign_id)
    User_Campaign.objects.get(user=user, campaign=campaign).donation_amount -= point_amount
    
    payload = {
        "orderIdentifier" : str(user.username)+"USER_redeem "+str(user_custom.donation_count+1)+"to Campaign "+str(campaign_id),
        "userIdentifier" : str(user.password),
        "loyaltyProgramId" : "1564707676167177217",
        "amount" : str(point_amount),
        "description" : str(timezone.now()) + " "+ str(user.username)+" "+ str(point_amount) + " 포인트 차감"
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
    url = "https://api.luniverse.io/svc/v2/mercury/point-accounts/"+str(user.password)+"/balances/MEAL"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.get(url, headers=headers)
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
def listPointHistories(request):
    user = define_user(request)
    url = "https://api.luniverse.io/svc/v2/mercury/point/histories?userIdentifier="+str(user.password)+"&loyaltyProgramId=1564707676167177217&rpp=50&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.get(url, headers=headers)
    return Response(response, status=status.HTTP_200_OK)