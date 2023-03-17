from django.db import models
from user.models import User
# Create your models here.

class User_Record(models.Model):
    userrecord_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_budget = models.IntegerField()
    today_date = models.DateTimeField()
    comsumption = models.IntegerField()
    donation = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'User_Record'
    

class Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    userrecord = models.ForeignKey(User_Record, on_delete=models.CASCADE)
    when = models.CharField(max_length=10)
    category = models.CharField(max_length=30)
    price = models.IntegerField()
    memo = models.TextField()
    settlement = models.BooleanField()
    
    class Meta:
        managed = False
        db_table = 'Record'