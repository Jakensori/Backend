from django.db import models
from user.models import User
# Create your models here.

class Donation_Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField()
    expiry_date = models.DateTimeField()
    description = models.TextField()
    created_at = models.DateTimeField()