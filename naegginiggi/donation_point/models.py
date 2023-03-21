from django.db import models
from user.models import User
# Create your models here.

class Donation_Point(models.Model):
    donation_point_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    point = models.IntegerField()
    expiry_date = models.DateTimeField()
    description = models.TextField()
    created_at = models.DateTimeField()
    
    class Meta:
        managed = True
        db_table = 'Donation_Point'