from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import RegisterSerializer

from django.contrib.auth.models import User as uu
from django.shortcuts import get_object_or_404
from rest_framework import status
from . import models
from user.models import User
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

@api_view(['GET','DELETE'])
def get_delete_user_data(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user
        if request.method == 'GET':  
            return Response({
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'password': user.password,
                },
            })
        elif request.method == 'DELETE':
            # auth의 User가 삭제되면 Model의 User 또한 삭제됨 (CASCADE)
            user = get_object_or_404(User, id=request.user.id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'not authenticated'}, status=400)
    

@api_view(['POST'])
def register_api(request):
    # auth의 User 저장
    serializer = RegisterSerializer(data={'username': request.data['userid'], 'email': request.data['email'], 'password': request.data['password']})
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    myuser = models.User(user=user, username=request.data['username'])
    myuser.save() # Model의 User Entity 저장 (auth의 User와 1대 1 매핑으로 연결되어있음)
    
    return Response({
        'user_info': {'id': user.id,
            'userid': user.username,
            'email': user.email,
            'username': myuser.username}
    })
    
    
# 아이디 중복 체크
@api_view(['POST'])
def duplicationcheck(request):
    userid = request.data['userid']
    try:
        user = get_object_or_404(uu, username=userid)
    except:
        return Response(False, status=status.HTTP_200_OK)
    return Response(True, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def patch_username(request):
    user, username_to_change= get_object_or_404(models.User, user=request.user), request.data['username']
    user.username = username_to_change
    user.save()
    return Response(status=status.HTTP_200_OK)
