from rest_framework import serializers
from donation_point.models import Donation_Point


class DonationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation_Point
        fields = '__all__'
