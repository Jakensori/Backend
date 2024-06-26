from django.db import models
from user.models import User

# Create your models here.
class User_Custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    month_budget = models.IntegerField()
    donation_temperature = models.IntegerField(default=0) # mealpoint (사용자가 기부할 때 지급됨)
    total_donation = models.IntegerField(default=0)
    donation_count = models.IntegerField(default=0)
    savings = models.IntegerField(default=0) # 기부 저금통 금액
    authority = models.BooleanField(default=False) ## 초기 값 : 0 == 기부자 // 1 == 재단
    
    class Meta:
        managed = True
        db_table = 'User_Custom'
