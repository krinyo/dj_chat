# Generated by Django 5.0.1 on 2024-02-05 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(default='test chat', max_length=255),
        ),
    ]
