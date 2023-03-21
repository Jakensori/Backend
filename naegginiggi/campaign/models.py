from django.db import models
from user.models import User

# Create your models here.
class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    rdonaBoxNo = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    summary = models.TextField()
    hlogName= models.CharField(max_length=50)
    startYmd = models.DateTimeField()
    endYmd = models.DateTimeField()
    currentAmount = models.IntegerField()
    donationCount = models.IntegerField()
    goalAmount = models.IntegerField()
    
    class Meta:
        managed = True
        db_table = 'Campaign'
    

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    class Meta:
        managed = True
        db_table = 'Review'
    

class User_Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    donation_amount = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'User_Campaign'
    
    
# user_campaign 테이블이 없으면 message 테이블도 생성되지 못하게 하기 !! -> 해당 캠페인에 기부한 회원만 대화 참여 가능
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    
    class Meta:
        managed = True
        db_table = 'Message'