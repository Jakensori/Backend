from django.db import models
from user.models import User
# Create your models here.

class User_Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_budget = models.IntegerField()
    today_date = models.DateTimeField()
    comsumption = models.IntegerField()
    donation = models.IntegerField()
    

class Record(models.Model):
    user_record = models.ForeignKey(User_Record, on_delete=models.CASCADE)
    when = models.CharField(max_length=10)
    category = models.CharField(max_length=30)
    price = models.IntegerField()
    memo = models.TextField()
    settlement = models.BooleanField()