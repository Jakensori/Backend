from django.db import models
from user.models import User

# Create your models here.
class User_Custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    month_budget = models.IntegerField()
    donation_temperature = models.IntegerField(default=0)
    total_donation = models.IntegerField(default=0)
    donation_count = models.IntegerField(default=0)
    
    class Meta:
        managed = False
        db_table = 'User_Custom'