from django.db import models
from user.models import User

# Create your models here.
class User_Custom(models.Model):
    custom_user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    month_budget = models.IntegerField()
    donation_temperature = models.IntegerField()
    total_donation = models.IntegerField()
    donation_count = models.IntegerField(default=0)
    
    class Meta:
        managed = False
        db_table = 'User_Custom'