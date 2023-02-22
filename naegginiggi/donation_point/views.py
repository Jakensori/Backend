from django.shortcuts import get_object_or_404
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from knox.auth import TokenAuthentication

from user_custom.models import User_Custom
# Create your views here.
def index(request) :
    return render(request, 'kakaopay_redirectPage.html')


@api_view(['POST'])
def accumulatePointByUserId(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    token = str(token).split()[1].encode("utf-8")
    knoxAuth = TokenAuthentication()
    user, auth_token = knoxAuth.authenticate_credentials(token)
    url = "https://api.luniverse.io/svc/v2/mercury/point/save"
    point_amount = request.data['point']
    user_custom = get_object_or_404(User_Custom, user = user)
    
    payload = {
        "orderIdentifier" : str(user.username)+"USER_add "+str(user_custom.donation_count+1),
        "userIdentifier" : str(token),
        "loyaltyProgramId" : "1564707676167177217",
        "amount" : str(point_amount),
        "description" : str(timezone.now()) + " "+ str(user.username)+" "+ str(point_amount) + " 포인트 충전"
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
    token = request.META.get('HTTP_AUTHORIZATION', False)
    token = str(token).split()[1].encode("utf-8")
    knoxAuth = TokenAuthentication()
    user, auth_token = knoxAuth.authenticate_credentials(token)
    url = "https://api.luniverse.io/svc/v2/mercury/point/spend"
    point_amount = request.data['point']
    user_custom = get_object_or_404(User_Custom, user = user)
    
    payload = {
        "orderIdentifier" : str(user.username)+"USER_redeem "+str(user_custom.donation_count+1),
        "userIdentifier" : str(token),
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
    token = request.META.get('HTTP_AUTHORIZATION', False)
    token = str(token).split()[1].encode("utf-8")
    url = "https://api.luniverse.io/svc/v2/mercury/point-accounts/"+str(token)+"/balances/MEAL"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.get(url, headers=headers)
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
def listPointHistories(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    token = str(token).split()[1].encode("utf-8")
    url = "https://api.luniverse.io/svc/v2/mercury/point/histories?userIdentifier="+str(token)+"&loyaltyProgramId=1564707676167177217&rpp=50&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ2ZXIiOiJ2MSIsInRrbiI6ImI4ZjgzY2NkZGIyZTU5MjkiLCJ0cGUiOiJJQU0iLCJzbHQiOiJlYzQyZjkwMTJjMjFjYTA3IiwiaWF0IjoxNjc2NTI2MTQxLCJleHAiOjE2NzcxMzA5NDEsImlzcyI6Imx1bnZzOmJhYXM6YXV0aDpzZXJ2aWNlIn0.8b4rysCN1x5x88YjAWhdnivVAJc6o7ReKuUUCzEyEGX9pD0ASOewdvGPHwyHHVIjAf-x-U15pkyk67N09JNisQ"
    }
    response = requests.get(url, headers=headers)
    return Response(response, status=status.HTTP_200_OK)