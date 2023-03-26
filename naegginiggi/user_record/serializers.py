from rest_framework import serializers
from user_record.models import User_Record, Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        exclude = ('record_id','settlement','userrecord',)


class User_RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Record
        exclude = ('userrecord_id', 'today_date', 'donation', 'user','differ',)
        
        
class AccountBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Record
        exclude = ('userrecord_id', 'day_budget', 'comsumption', 'user',)