from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Record, User_Record
from user_custom.models import User_Custom
from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from knox.auth import TokenAuthentication
from .serializers import RecordSerializer, User_RecordSerializer

# 날짜 계산
from datetime import datetime
from dateutil.relativedelta import *

# Create your views here.
@api_view(['GET'])
def todayrecord(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user
        
    user = get_object_or_404(User,user=user) 
    user_record=User_Record.objects.get(user=user, today_date=datetime.today().date())
    records=Record.objects.filter(userrecord=user_record)
    records_serializer = RecordSerializer(records, many=True).data
    user_record_serializer = User_RecordSerializer(user_record).data
    return Response({"끼니 기록들": records_serializer, "하루 기록정보": user_record_serializer}, status=status.HTTP_200_OK)
    
    
@api_view(['POST', 'GET'])    
def todaysettlement(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user
    user = get_object_or_404(User,user=user) 
    user_detail = User_Custom.objects.get(user=user)
    user_record=User_Record.objects.get(user=user, today_date=datetime.today().date())
    if request.method == 'POST':  # 하루 기부금 저장
        today_donation = request.data['today_donation']
        user_record.donation += int(today_donation)
        
        user_detail.donation_count += 1
        user_detail.donation_temperature += 10
        user_detail.total_donation += int(today_donation)
        
        user_record.save()
        user_detail.save()
        return Response({"today_donation": user_record.donation}, status=status.HTTP_200_OK)
        
    else:  # 하루정산 하기 전 기부가능 금액 고지
        record=Record.objects.filter(userrecord=user_record)
        donation=user_record.day_budget-user_record.comsumption
        return Response({"count":record.count(), "donation_possible": donation}, status=status.HTTP_200_OK)
        
        
@api_view(['POST'])     
def addrecord(request):  # 하나의 record 테이블 생성
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user
        
    user = get_object_or_404(User,user=user) 
    user_detail = User_Custom.objects.get(user=user)
    today = datetime.today()
    next_month = datetime(today.year, today.month, 1) + relativedelta(months=1)
    this_month_last_day = next_month + relativedelta(seconds=-1)
    day_budget=int(user_detail.month_budget//this_month_last_day.day)
    
    if User_Record.objects.filter(user=user, today_date=today.date()).exists():
        user_record=User_Record.objects.get(user=user, today_date=today.date())
    else:
        user_record=User_Record.objects.create(
            user=user,
            day_budget=day_budget,
            today_date=today.date(),
            comsumption=0,
            donation=0
        )
    record = Record.objects.create(
        userrecord=user_record,
        when=request.data['when'],
        category=request.data['category'],
        price=request.data['price'],
        memo=request.data['memo']
    )
    user_record.comsumption += request.data['price']
    user_record.save()
    return Response({'add_record': record.when}, status=status.HTTP_200_OK)
