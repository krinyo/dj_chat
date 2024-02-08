from django.shortcuts import render
from .models import Chat, Message, SkippedMessage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from asgiref.sync import sync_to_async
from django.template.response import TemplateResponse


@login_required
def get_new_message_counts(request):
    chats = Chat.objects.all()
    skipped_messages = SkippedMessage.objects.filter(chat__in=chats, user=request.user)
    new_message_counts = {skipped.chat.pk: skipped.count for skipped in skipped_messages}
    return JsonResponse(new_message_counts)


@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    UserModel = get_user_model()
    all_users = UserModel.objects.all()
    skipped_messages = SkippedMessage.objects.filter(user=request.user)
    return render(request, 'chats/chat_list.html', {'chats': chats, 'username': request.user.username, 'all_users' : all_users, 'skipped_messages' : skipped_messages})


@login_required
def chat_detail(request, pk):
    chat = Chat.objects.get(pk=pk)
    skipped, created = SkippedMessage.objects.get_or_create(chat=chat, user=request.user)

    skipped.count = 0
    skipped.save()
    participants = chat.participants.all()  # Получаем всех участников чата
    return render(request, 'chats/chat_detail.html', {'chat': chat, 'username': request.user.username, 'participants': participants})


@csrf_exempt
def send_message(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_text = data.get('message')
        chat = Chat.objects.get(pk=pk)
        message = Message.objects.create(chat=chat, author=request.user, text=message_text)
        return JsonResponse({'message': message.text})

@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_name = data.get('name')
        participants = data.get('participants')
        # Создаем новый чат
        chat = Chat.objects.create(name=chat_name)

        # Получаем модель пользователя
        User = get_user_model()

        # Добавляем участников в чат
        for username in participants:
            try:
                user = User.objects.get(username=username)
                chat.participants.add(user)
            except User.DoesNotExist:
                pass  # Если пользователь не найден, просто пропустите его

        return JsonResponse({'status': 'ok', 'chat_id': chat.pk})