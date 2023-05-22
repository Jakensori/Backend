from django.db import models
from user.models import User
# Create your models here.

class Donation_Point(models.Model):
    donatitonpoint_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    paymentkey= models.CharField(max_length=200)
    approvedAt = models.DateTimeField()
    method=models.CharField(max_length=50)
    amount=models.IntegerField()
    orderId = models.CharField(max_length=100)
    
    class Meta:
        managed = True
        db_table = 'Donation_Point'
