import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
import django
django.setup()
from chats.models import Message, Chat  # Полный путь к вашей модели Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['url_route']['kwargs'])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group when the WebSocket is closed
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(self.scope['user'].username)
        print(text_data_json['room_name'])
        # Save the message to the database
        await self.save_message(message)

        # Send message to room group
        await self.send_group({
            'type': 'chat_message',
            'message': message,
            'username': self.scope['user'].username,
            'room_name': text_data_json['room_name']
        })
    @database_sync_to_async
    def save_message(self, message):
        # Save the message to the database using room_name
        try:
            chat = Chat.objects.get(room_name=self.room_name)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(room_name=self.room_name)

        Message.objects.create(text=message, chat=chat, author=self.scope["user"])
    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room_name = event['room_name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': f'{username}: {message}',
            'room_name': room_name  # Добавим информацию о комнате
        }))

    async def send_group(self, message):
        # Send message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            message
        )

