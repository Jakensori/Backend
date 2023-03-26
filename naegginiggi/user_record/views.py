from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Record, User_Record
from user_custom.models import User_Custom
from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from knox.auth import TokenAuthentication
from .serializers import RecordSerializer, User_RecordSerializer, AccountBookSerializer

# 날짜 계산
from datetime import datetime
from dateutil.relativedelta import *

# Create your views here.
@api_view(['GET'])
def todayrecord(request, user_id): 
    user = get_object_or_404(User,id=user_id) 
    # 수정
    user_record=User_Record.objects.get(user=user, today_date="2023-03-23")
    records=Record.objects.filter(userrecord=user_record)
    records_serializer = RecordSerializer(records, many=True).data
    user_record_serializer = User_RecordSerializer(user_record).data
    return Response({"끼니 기록들": records_serializer, "하루 기록정보": user_record_serializer}, status=status.HTTP_200_OK)
    
    
@api_view(['POST', 'GET'])    
def todaysettlement(request, user_id):
    user = get_object_or_404(User,id=user_id)
    user_detail = User_Custom.objects.get(user=user)
    # 수정
    user_record=User_Record.objects.get(user=user, today_date="2023-03-22")
    differ=user_record.day_budget-user_record.comsumption
    if request.method == 'POST':  # 하루 기부금 저장
        today_donation = request.data["today_donation"]
        user_record.donation += int(today_donation)
        user_record.differ = differ
        for i in Record.objects.filter(userrecord=user_record):
            i.settlement = True
            i.save()
        user_detail.donation_count += 1
        user_detail.donation_temperature += 10
        user_detail.total_donation += int(today_donation)
        
        user_record.save()
        user_detail.save()
        return Response({"today_donation": user_record.donation}, status=status.HTTP_200_OK)
        
    else:  # 하루정산 하기 전 기부가능 금액 고지
        record=Record.objects.filter(userrecord=user_record)
        if differ >= 0:
            donation=differ
        else:
            donation=0
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


@api_view(['GET'])
def month_accountbook(request):
    token = request.META.get('HTTP_AUTHORIZATION', False)
    if token:
        token = str(token).split()[1].encode("utf-8")
        knoxAuth = TokenAuthentication()
        user, auth_token = knoxAuth.authenticate_credentials(token)
        request.user = user
        
    # 프론트랑 연결할 때는 request.GET으로 고치기
    year = int(request.data['year'])
    month = int(request.data['month'])
    
    user = get_object_or_404(User,user=user)
    user_record = User_Record.objects.filter(user=user)
    for i in user_record:
        if i.today_date.year == year and i.today_date.month == month:
            pass
        else:
            user_record= user_record.exclude(userrecord_id=i.userrecord_id)
            
    month_budget = User_Custom.objects.get(user=user).month_budget  # 한 달 예산
    all_comsumption = 0
    all_donation = 0
    userrecord_serializer = AccountBookSerializer(user_record, many=True).data
    
    for i in user_record:
        all_comsumption += i.comsumption
        all_donation += i.donation
        
    return Response({'하루 기록들': userrecord_serializer, '총 소비금': all_comsumption, '총 기부금': all_donation, '한 달 예산': month_budget, '남은 금액': month_budget-all_comsumption}, status=status.HTTP_200_OK)
    
   
def analysis(request, user_id):
    user = get_object_or_404(User,id=user_id)
    year = int(request.GET['year'])
    month = int(request.GET['month']) # 입력 값이 0일때는 '전체'로 조회하기
    userrecord_temp = []
    user_record=User_Record.objects.filter(user=user)
    if month == 0:
        for i in user_record:
            if i.today_date.year == year:
                userrecord_temp.append(i)
    else:
        for i in user_record:
            if i.today_date.year == year and i.today_date.month == month:
                userrecord_temp.append(i)
                
    return userrecord_temp 


@api_view(['GET'])     
def category_analysis(request,user_id):
    userrecord_temp=analysis(request,user_id)
    record_temp = {}
    total_count=0
    for i in userrecord_temp:
        records = Record.objects.filter(userrecord=i, settlement=True)
        total_count += records.count()
        for j in records:
            if j.category in record_temp:
                record_temp[j.category] += 1
            else:
                record_temp[j.category] = 1
            
    return Response({"record_byCategory": record_temp, "total_count": total_count}, status=status.HTTP_200_OK)
    
@api_view(['GET'])  
def time_analysis(request,user_id):        
    userrecord_temp=analysis(request,user_id)
    record_temp = {}
    total_count = 0
    for i in userrecord_temp:
        records = Record.objects.filter(userrecord=i, settlement=True)
        total_count += records.count()
        for j in records:
            if j.when in record_temp:
                record_temp[j.when] += 1
            else:
                record_temp[j.when] = 1
            
    return Response({"record_byTime": record_temp, "total_count": total_count}, status=status.HTTP_200_OK)