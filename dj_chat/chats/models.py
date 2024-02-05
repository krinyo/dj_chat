from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    room_name = models.AutoField(primary_key=True)  # Добавьте поле room_name
    name = models.CharField(max_length=255, default='test chat')
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
