# Generated by Django 5.0.1 on 2024-02-05 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_chat_room_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='id',
        ),
        migrations.AlterField(
            model_name='chat',
            name='room_name',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]