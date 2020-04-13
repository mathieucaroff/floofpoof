# Generated by Django 3.0.5 on 2020-04-10 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users_chat', '0005_chatmessage_thread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatmessage', to=settings.AUTH_USER_MODEL, verbose_name='sender'),
        ),
    ]
