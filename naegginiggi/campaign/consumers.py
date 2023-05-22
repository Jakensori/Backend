from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async  # db 접근
import json
from user.models import User
from campaign.models import Message, Campaign
from django.shortcuts import get_object_or_404


# 임의의 유저 가정
# user = get_object_or_404(User, id=1)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        await self.create_message(message)
        
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    @database_sync_to_async
    def create_message(self, message):
        user = get_object_or_404(User,id=1)
        Message.objects.create(
                user=user, campaign=get_object_or_404(Campaign, campaign_id=int(self.room_name)), message=message
        )
        return True
