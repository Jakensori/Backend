from .models import User_Custom
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from knox.auth import AuthToken, TokenAuthentication
from django.db import connection

# Create your views here.
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