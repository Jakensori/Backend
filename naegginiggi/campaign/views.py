from django.shortcuts import render
from .models import Campaign
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.safestring import mark_safe
import json
# Create your views here.

## 비동기 실시간 챗 구현

def index(request):
    return render(request, 'campaign/index.html', {})


def room(request, room_name):
    return render(request, 'campaign/chat_room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })