import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
import django
django.setup()
from chats.models import Message, Chat, SkippedMessage # Полный путь к вашей модели Message
from asgiref.sync import sync_to_async

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
            'username': username,  # Отправляем username отдельно
            'message': message,  # Отправляем message отдельно
            'room_name': room_name  # Добавим информацию о комнате
        }))


    async def send_group(self, message):
        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            message
        )

        # Увеличиваем счетчик пропущенных сообщений для всех участников чата
        await self.increase_skipped_message_count(message['room_name'])


    async def increase_skipped_message_count(self, room_name):
        # Получаем чат
        chat = await sync_to_async(Chat.objects.get)(room_name=room_name)

        # Получаем всех участников чата
        participants = await sync_to_async(list)(chat.participants.exclude(username=self.scope['user'].username))

        # Для каждого участника увеличиваем счетчик пропущенных сообщений
        for participant in participants:
            # Проверяем, существует ли уже запись SkippedMessage для этого пользователя и чата
            skipped_message, created = await sync_to_async(SkippedMessage.objects.get_or_create)(user=participant, chat=chat)
            # Если запись уже существует, увеличиваем счетчик пропущенных сообщений
            if not created:
                skipped_message.count += 1
                await sync_to_async(skipped_message.save)()
        


