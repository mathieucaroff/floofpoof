import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from login.models import User
from .models import Thread, ChatMessage
from datetime import datetime

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        print("connected", event)

        await self.send({
            "type": "websocket.accept"
        })

        me = self.scope['user']
        other_user = await self.get_other_user()
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

    async def websocket_receive(self,event):
        
        print("received", event)
        front_txt = event.get('text', None)
        if front_txt is not None:
            loaded_dict_data = json.loads(front_txt)
            msg = loaded_dict_data.get('message')
            timestamp = str(datetime.now().strftime("%B %d, %Y, %I:%M %p"))
            me = self.scope['user']
            username= 'not_auth'
            if me.is_authenticated:
                username = me.__str__()
            myResponse = {
                'message': msg,
                'username': username,
                'timestamp': timestamp
            }

            await self.create_chat_message(me, msg)

            #broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )
    
    async def chat_message(self,event):
        #sends the message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self,event):
        print("disconnected", event)
    
    @database_sync_to_async
    def get_thread(self, user, other_user):
        return Thread.objects.get_or_new(user, other_user)[0]
    
    @database_sync_to_async
    def get_other_user(self):
        return User.objects.get(id= self.scope['url_route']['kwargs']['otherId'])
    
    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread= thread_obj, user= me, message= msg)