cd dj_chat
export DJANGO_SETTINGS_MODULE="dj_chat.settings"
daphne -b 0.0.0.0 -p 8000 dj_chat.asgi:application