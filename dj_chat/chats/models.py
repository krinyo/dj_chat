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

class SkippedMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} - {self.chat.name}: {self.count} skipped messages'