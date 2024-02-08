Django chatter.
Installation:

    git clone https://github.com/krinyo/dj_chat
    cd dj_chat
    bash install.sh
    source venv/bin/activate
    cd dj_chat
    export DJANGO_SETTINGS_MODULE="dj_chat.settings"
    daphne -b 0.0.0.0 -p 8000 dj_chat.asgi:application

![image](https://github.com/krinyo/dj_chat/assets/57134381/a74bdd7e-5b99-4231-85b8-17c7976a8fe7)
