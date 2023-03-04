from django.shortcuts import render
from .models import Campaign
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


def chat(request):
    return render('campaign/chat_room.html')