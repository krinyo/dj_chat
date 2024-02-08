Django chatter.
Installation:
    git clone https://github.com/krinyo/dj_chat
    cd dj_chat
    bash install.sh
    source venv/bin/activate
    cd dj_chat
    export DJANGO_SETTINGS_MODULE="dj_chat.settings"
    daphne -b 0.0.0.0 -p 8000 dj_chat.asgi:application