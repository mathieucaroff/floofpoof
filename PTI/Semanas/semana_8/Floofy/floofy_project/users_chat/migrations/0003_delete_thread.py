# Generated by Django 3.0.5 on 2020-04-09 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_chat', '0002_thread'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Thread',
        ),
    ]
