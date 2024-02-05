from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'chats/chat_list.html', {'chats': chats, 'username': request.user.username})

@login_required
def chat_detail(request, pk):
    chat = Chat.objects.get(pk=pk)
    return render(request, 'chats/chat_detail.html', {'chat': chat, 'username': request.user.username})

@csrf_exempt
def send_message(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_text = data.get('message')
        chat = Chat.objects.get(pk=pk)
        message = Message.objects.create(chat=chat, author=request.user, text=message_text)
        return JsonResponse({'message': message.text})
