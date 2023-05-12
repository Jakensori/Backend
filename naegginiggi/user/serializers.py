from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.db import models
from django.db.models import fields
from rest_framework import serializers

from . import models    
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

        extra_kwargs = {
            "password": {"write_only":True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators":[
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already exists"
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user