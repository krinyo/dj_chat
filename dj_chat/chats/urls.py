from django.urls import path, include, re_path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('chats/', views.chat_list, name='chat_list'),
    path('chats/chat_<int:pk>/', views.chat_detail, name='chat_detail'),
    path('chats/chat_<int:pk>/send_message/', views.send_message, name='send_message'),
    path('chats/create_chat/', views.create_chat, name='create_chat'),
    re_path(r'^$', RedirectView.as_view(url='/chats/', permanent=True)),
]
