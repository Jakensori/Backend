from django.db import models
from user.models import User

# Create your models here.
class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    rdonaBoxNo = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.ImageField()
    summary = models.TextField()
    hlogName= models.CharField(max_length=50)
    startYmd = models.DateTimeField()
    endYmd = models.DateTimeField()
    currentAmount = models.IntegerField()
    donationCount = models.IntegerField()
    goalAmount = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'Campaign'
    

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'Review'
    

class User_Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'User_Campaign'
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    message = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'Message'