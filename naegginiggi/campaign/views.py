from django.shortcuts import render

# Create your views here.
def index(request):
    return render('campaign/index.html')


def chat(request):
    return render('campaign/chat_room.html')