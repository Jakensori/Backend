from django.db import models
from user.models import User

# Create your models here.
class Campaign(models.Model):
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
    

class Review(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    

class User_Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    message = models.TextField()