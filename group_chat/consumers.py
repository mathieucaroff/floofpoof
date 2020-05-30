import asyncio
import json
from datetime import datetime
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async


from .models import Thread, Message
from login.models import User

class GroupChatConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print("connected", event)

        await self.send({
            "type": "websocket.accept"
        })

        groupId = self.scope['url_route']['kwargs']['groupId']
        thread_obj = await self.get_thread(groupId)
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
            senderId = loaded_dict_data.get('from')
            sender = await self.get_user(senderId)
            timestamp = str(datetime.now().strftime("%B %d, %Y, %I:%M %p"))

            sender_name= 'not_auth'
            if sender.is_authenticated:
                sender_name = sender.__str__()
            myResponse = {
                'message': msg,
                'sender_name': sender_name,
                'timestamp': timestamp
            }

            await self.create_message(sender, msg)

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
    def get_thread(self, groupId):
        return Thread.objects.get_or_new(groupId)[0]

    @database_sync_to_async
    def get_user(self, senderId):
        return User.objects.get(id=senderId)

    @database_sync_to_async
    def create_message(self, me, msg):
        thread_obj = self.thread_obj
        return Message.objects.create(thread= thread_obj, user= me, message= msg)