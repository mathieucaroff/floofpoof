from django.db import models
from login.models import *
from django.conf import settings
from django.db.models import Q

class ThreadManager(models.Manager):

    def get_or_new(self, groupId): # get_or_create
        myGroup = Group.objects.get(id=groupId)
        if Thread.objects.filter(group=myGroup).exists():
            thread = Thread.objects.get(group=myGroup)
            return thread, False
        else:
            obj = self.model(group = myGroup)
            obj.save()
            return obj, True

class Thread(models.Model):

    class Meta:
        managed=True
        db_table = 'group_chat_thread'

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_chat_thread')
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    
    objects      = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False

class Message(models.Model):

    class Meta:
        managed=True
        db_table = 'group_chat_message'

    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)