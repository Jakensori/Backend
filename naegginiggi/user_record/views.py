from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Record, User_Record
from user_custom.models import User_Custom
from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from knox.auth import TokenAuthentication
from .serializers import RecordSerializer, AccountBookSerializer

# 날짜 계산
from datetime import datetime, date
from django.utils import timezone
from dateutil.relativedelta import *

# Create your views here.
# 오늘의 식사 기록 불러오기
@api_view(['GET'])
def todayrecord(request, user_id): 
    user = get_object_or_404(User,id=user_id) 
    # 수정
    year=int(request.GET['year'])
    month=int(request.GET['month'])
    day=int(request.GET['day'])
    input_date=str(date(year,month,day))
    if User_Record.objects.filter(user=user, today_date=input_date).exists(): # 식사 기록이 하나 이상 존재할 때
        user_record=User_Record.objects.get(user=user, today_date=input_date)
        records=Record.objects.filter(userrecord=user_record)
        records_serializer = RecordSerializer(records, many=True).data
        day_budget = user_record.day_budget
        comsumption = user_record.comsumption
        return Response({"records": records_serializer, "day_budget": day_budget,"comsumption":comsumption}, status=status.HTTP_200_OK)
    else: # 당일에 식사 기록이 없을 때
        user_detail = User_Custom.objects.get(user=user)
        today = datetime.today()
        next_month = datetime(today.year, today.month, 1) + relativedelta(months=1)
        this_month_last_day = next_month + relativedelta(seconds=-1)
        day_budget=int(user_detail.month_budget//this_month_last_day.day) # 하루 식비 예산 계산
        return Response({"day_budget":day_budget,"comsumption":0}, status=status.HTTP_200_OK)


# 식사 기록 끝난 후, 하루 식비 정산하기
@api_view(['POST', 'GET'])    
def todaysettlement(request, user_id):
    user = get_object_or_404(User,id=user_id)
    user_detail = User_Custom.objects.get(user=user)

    year=int(request.GET['year'])
    month=int(request.GET['month'])
    day=int(request.GET['day'])
    input_date=str(date(year,month,day))
    user_record=User_Record.objects.get(user=user, today_date=input_date)
    differ=user_record.day_budget-user_record.comsumption # 하루 예산 - 당일 소비 금액
    if request.method == 'POST':  # 하루 저금액 저장
        today_donation = request.data["today_donation"] # 저금 가능 금액 중 기부할 금액 입력
        user_record.donation += int(today_donation)
        user_record.differ = differ
        for i in Record.objects.filter(userrecord=user_record):
            i.settlement = True
            i.save()
        user_detail.savings += int(today_donation) # 기부 저금통에 당일 기부 금액 저장
        user_record.save()
        user_detail.save()
        return Response(status=status.HTTP_200_OK)
        
    else:  # 하루정산 하기 전 기부가능 금액 고지
        record=Record.objects.filter(userrecord=user_record)
        if differ >= 0:
            donation=differ
        else:
            donation=0
        return Response({"count":record.count(), "donation_possible": donation}, status=status.HTTP_200_OK)
        

 # 식사 기록 생성하기       
@api_view(['POST'])     
def addrecord(request,user_id):  # 하나의 record 테이블 생성
    #token = request.META.get('HTTP_AUTHORIZATION', False)
    #if token:
    #    token = str(token).split()[1].encode("utf-8")
    #    knoxAuth = TokenAuthentication()
    #    user, auth_token = knoxAuth.authenticate_credentials(token)
    #    request.user = user
        
    #   user = get_object_or_404(User,user=user) 
    # 임의 유저 설정
    user = get_object_or_404(User,id=user_id)
    user_detail = User_Custom.objects.get(user=user)
    today = timezone.now()
    next_month = datetime(today.year, today.month, 1) + relativedelta(months=1)
    this_month_last_day = next_month + relativedelta(seconds=-1)
    day_budget=int(user_detail.month_budget//this_month_last_day.day)
    
    if User_Record.objects.filter(user=user, today_date=today.date()).exists(): # 당일에 식사 기록이 하나 이상 존재할 때
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


# 한 달 가계부 한꺼번에 불러오기
@api_view(['GET'])
def month_accountbook(request,user_id):
    #token = request.META.get('HTTP_AUTHORIZATION', False)
    #if token:
    #    token = str(token).split()[1].encode("utf-8")
    #    knoxAuth = TokenAuthentication()
    #    user, auth_token = knoxAuth.authenticate_credentials(token)
    #    request.user = user
        
    # 프론트랑 연결할 때는 request.GET으로 고치기
    year = int(request.GET['year'])
    month = int(request.GET['month'])
    # 임의 유저
    user = get_object_or_404(User,id=user_id)
    user_record = User_Record.objects.filter(user=user)
    
    for i in user_record:
        if i.today_date.year == year and i.today_date.month == month:
            pass
        else:
            user_record= user_record.exclude(userrecord_id=i.userrecord_id)
            
    month_budget = User_Custom.objects.get(user=user).month_budget  # 한 달 예산
    all_comsumption = 0 # 값 초기화
    all_donation = 0 # 값 초기화
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


# 식사 카테고리 분석 불러오기 (예: 외식, 배달, 등등)
@api_view(['GET'])     
def category_analysis(request,user_id):
    userrecord_temp=analysis(request,user_id)
    record_temp = {}
    total_count=0
    for i in userrecord_temp:
        records = Record.objects.filter(userrecord=i, settlement=True) # 정산 완료한 식사 기록만 불러오기
        total_count += records.count()
        for j in records:
            if j.category in record_temp:
                record_temp[j.category][0] += 1
                record_temp[j.category][1] += j.price 
            else:
                each_list=[1,j.price]
                record_temp[j.category] = each_list
            
    return Response({"record_byCategory": record_temp, "total_count": total_count}, status=status.HTTP_200_OK)


# 식사 시간 분석 불러오기 (예: 아침, 점심, 간식, 야식, 등등)
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
