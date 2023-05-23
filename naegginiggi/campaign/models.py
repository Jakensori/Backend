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
       
class Notification(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    createdAt = models.DateField()
    title = models.CharField(max_length=200)
    foundation = models.CharField(max_length=50)
    content = models.TextField()
    image = models.CharField(max_length=200)
    
    class Meta:
        managed=True
        db_table='Notification'


class User_Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    donation_amount = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'User_Campaign'   
