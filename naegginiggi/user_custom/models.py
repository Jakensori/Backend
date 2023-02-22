from django.db import models
from user.models import User

# Create your models here.
class User_Custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    month_budget = models.IntegerField()
    donation_temperature = models.IntegerField()
    total_donation = models.IntegerField()
    donation_count = models.IntegerField(null=True)