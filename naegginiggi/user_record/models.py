from django.db import models
from user.models import User
# Create your models here.

class User_Record(models.Model):
    userrecord_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    day_budget = models.IntegerField()
    today_date = models.DateField()
    comsumption = models.IntegerField()
    donation = models.IntegerField()
    differ = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'User_Record'
    

class Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    userrecord = models.ForeignKey(User_Record, on_delete=models.CASCADE, null=True)
    when = models.CharField(max_length=10)
    category = models.CharField(max_length=30)
    price = models.IntegerField()
    memo = models.TextField(null=True)
    settlement = models.BooleanField(default=False) # 하루 정산 여부
    
    class Meta:
        managed = True
        db_table = 'Record'
