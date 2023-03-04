from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import RegisterSerializer

from . import models

# Create your views here.
@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    
    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
            },
        'token': token
    })

@api_view(['GET'])
def get_user_data(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password,
            },
        })
    return Response({'error': 'not authenticated'}, status=400)

@api_view(['POST'])
def register_api(request):
    # auth의 User 저장
    serializer = RegisterSerializer(data={'username': request.data['userid'], 'email': request.data['email'], 'password': request.data['password']})
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    _, token = AuthToken.objects.create(user) 
    
    username = request.data['username']
    
    return Response({
        'user_info': {'id': user.id,
            'userid': user.username,
            'email': user.email,
            'username': username},
        
        'token': token
    })
