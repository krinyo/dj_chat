# Generated by Django 5.0.1 on 2024-02-07 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0005_skippedmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skippedmessage',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
