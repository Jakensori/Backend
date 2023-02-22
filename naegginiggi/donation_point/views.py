from django.shortcuts import render
import requests
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from rest_framework.authtoken.models import Token
# Create your views here.
def index(request) :
    return render(request, 'kakaopay_redirectPage.html')


@api_view(['POST'])
def accumulatePointByUserId(request):
    user = get_object_or_404(User, user=request.user)
    token = Token.objects.get(user=user)
    url = "https://api.luniverse.io/svc/v2/mercury/point/save"

    payload = {
        "orderIdentifier" : "",
        "userIdentifier" : str(token),
        "loyaltyProgramId" : "1564707676167177217",
        
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer AUTH-TOKEN"
    }

    response = requests.post(url, headers=headers)

    print(response.text)