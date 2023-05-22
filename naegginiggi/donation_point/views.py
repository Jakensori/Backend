from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from knox.auth import TokenAuthentication

import my_settings

from user.models import User
from user_custom.models import User_Custom
from campaign.models import User_Campaign, Campaign

from donation_point.models import Donation_Point
from .serializers import DonationPointSerializer
import uuid
import base64
import codecs

# Create your views here.
apikey = my_settings.API_key_Purpose
accesskey = my_settings.Access_Key
secret = my_settings.Loyalty_Point_Secret
TOSSPAY_clientkey = 'test_ck_jkYG57Eba3GqKKZbqX5rpWDOxmA1'
TOSSPAY_Secretkey = 'test_sk_lpP2YxJ4K87xYYAAKR03RGZwXLOb'

def define_user(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    token = str(token).split()[1].encode("utf-8")
    knoxAuth = TokenAuthentication()
    user, auth_token = knoxAuth.authenticate_credentials(token)
    return user

# WUJtQT09와 같은 형태로 랜덤 코드 생성 함수
def generate_random_slug_code(length=15):  # length는 1-32사이에 존재해야 함.
    return base64.urlsafe_b64encode(       # url에서도 랜덤 코드를 사용가능하게 하기 위한 함수
        codecs.encode(uuid.uuid4().bytes, 'base64').rstrip() # base64로 인코딩
    ).decode()[:length] # 바이트스트링 타입을 문자열로 활용하기 위한 코드


def fail(request):
    return render('fail.html')

@api_view(['GET'])
def payments_request(request):
    payment_category = 0  # 0이면 카드, 1이면 가상계좌
    url = 'https://api.tosspayments.com/v1/payments'
    code = generate_random_slug_code()
    data = {"method" : "카드",
            "amount" : 3000,
            "orderId" : code,
            "orderName": "캠페인 3",
            "failUrl": "http://52.78.205.224:8000/donation/fail/",                          "successUrl": "http://52.78.205.224:8000/donation/approve/","customerName": "testuser"}
    headers = {'Authorization': 'Basic dGVzdF9za19scFAyWXhKNEs4N3hZWUFBS1IwM1JHWndYTE9iOg==', "Content-Type": "application/json"}
    res = requests.post(url, json=data, headers=headers)
    return Response(res)

@api_view(['GET'])
def payments_approve(request):
    url = 'https://api.tosspayments.com/v1/payments/confirm'
    data = {"orderId": request.GET['orderId'],
            "paymentKey": request.GET['paymentKey'],
            "amount": int(request.GET['amount'])}
    #authorization = TOSSPAY_Secretkey+':'
    #authorization = base64.b64encode(authorization.encode('ascii')).decode('ascii')
    #print(authorization)
    headers = {'Authorization': 'Basic dGVzdF9za19scFAyWXhKNEs4N3hZWUFBS1IwM1JHWndYTE9iOg==', "Content-Type": "application/json"}
    res = requests.post(url, json=data, headers=headers)
    res = res.json()
    # 임의 유저로 테스트
    user=get_object_or_404(User,id=1)
    campaign=Campaign.objects.get(campaign_id=3)
    if User_Campaign.objects.filter(user=user, campaign=campaign).exists():
        usercampaign=User_Campaign.objects.filter(user=user, campaign=campaign)
    else:
        usercampaign=User_Campaign.objects.create(
                user=user,
                campaign=campaign
        )
    donation_total = res['card']['amount']
    usercampaign.donation_amount += donation_total
    user_detail=User_Custom.objects.get(user=user)
    user_detail.donation_count += 1
    user_detail.total_donation += donation_total
    user_detail.donation_temperature += 20
    Donation_Point.objects.create(
        user=user,
        paymentkey=res["paymentKey"],
        approvedAt=res["approvedAt"],
        method=res["method"],
        amount=res["totalAmount"],
        orderId=res["orderId"]
    )
    accumulatePointByUserId(request,user,user_detail)
    return Response(res, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_account_info(request):
    paymentKey = request.data['paymentkey']
    url = 'https://api.tosspayments.com/v1/payments/'+paymentKey
    headers = {'Authorization': 'Basic dGVzdF9za19scFAyWXhKNEs4N3hZWUFBS1IwM1JHWndYTE9iOg=='}
    res = requests.get(url,headers=headers)
    return Response(res.json(), status=status.HTTP_200_OK)


#포인트 선결제 로직으로 생각하고 짠 함수임.
#포인트 환불을 의미.
@api_view(['POST'])
def cancel_payments(request):
    paymentKey=request.data['paymentKey']
    url = 'https://api.tosspayments.com/v1/payments/'+paymentKey+'/cancel'
    headers = {'Authorization': 'Basic dGVzdF9za19scFAyWXhKNEs4N3hZWUFBS1IwM1JHWndYTE9iOg==', "Content-Type": "application/json"}
    res = requests.post(url, json={'cancelReason':request.data['reason']}, headers=headers)
    return Response(res.json())


def get_authentication():
    tokenurl = "https://api.luniverse.io/svc/v2/auth-tokens"
    loyalty_program_id_url = "https://api.luniverse.io/svc/v2/mercury/loyalty-programs"
    payload = {
        "expiresIn":604800,
        "accessKey": accesskey,
        "secretKey" :secret
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }
    response = requests.post(tokenurl, json=payload, headers=headers)
    token = response.json()["data"]["authToken"]["token"]
    token_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer " + token
    }
    response = requests.get(loyalty_program_id_url, headers=token_headers)
    loyalty_program_id = response.json()["data"]["loyaltyPrograms"]["items"][0]["loyaltyProgramId"]
    return loyalty_program_id, token_headers


def accumulatePointByUserId(request,user,user_custom):
    loyalty_program_id, token_headers = get_authentication()
    earn_point_url = "https://api.luniverse.io/svc/v2/mercury/point/save"
    description = str(timezone.now()) + " " +str(user.username) + " "+  "20 포인트 충전"
    payload = {
        "orderIdentifier": generate_random_slug_code(),
        "userIdentifier": str(user.password),
        "loyaltyProgramId": loyalty_program_id,
        "amount": "20",
        "description": description,
    }
    response = requests.post(earn_point_url, json=payload, headers=token_headers)
    return Response(response.json(), status=status.HTTP_200_OK)


@api_view(['POST'])
def redeemPointByUserId(request):
    user = define_user(request)
    myuser = get_object_or_404(User, user_id=user.id)
    url = "https://api.luniverse.io/svc/v2/mercury/point/spend"
    loyalty_program_id, token_headers = get_authentication()
    using_point = request.data['used_point']
    user_custom = get_object_or_404(User_Custom, user=myuser)
    user_custom.donation_temperature -= using_point

    payload = {
        "orderIdentifier": generate_random_slug_code(),
        "userIdentifier": str(user.password),
        "loyaltyProgramId": loyalty_program_id,
        "amount": str(using_point),
        "description": str(timezone.now()) + " " + str(myuser.username)+" "+str(using_point) + " 포인트 차감"
    }
    response = requests.post(url, json=payload, headers=token_headers)
    return Response(response.json(), status=status.HTTP_200_OK)


@api_view(['GET'])
def listPointHistories(request):
    user = define_user(request)
    loyalty_program_id, token_headers = get_authentication()
    url = "https://api.luniverse.io/svc/v2/mercury/point/histories?userIdentifier=" + \
        str(user.password)+"&loyaltyProgramId="+str(loyalty_program_id)+"&rpp=50&page=1"
    response = requests.get(url, headers=token_headers)
    return Response(response.json(), status=status.HTTP_200_OK)


@api_view(['GET'])
def donation_receipt(request):
    # 임의 유저
    user = get_object_or_404(User,id=1)
    donation_user = Donation_Point.objects.filter(user=user)
    donation_list = DonationPointSerializer(donation_user, many=True).data
    return Response(donation_list, status=status.HTTP_200_OK)
