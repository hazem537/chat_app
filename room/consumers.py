import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync ,sync_to_async
from django.utils.functional import  SimpleLazyObject

Room = SimpleLazyObject(lambda: __import__('room.models', fromlist=['Room']).Room)
Message = SimpleLazyObject(lambda: __import__('room.models', fromlist=['Message']).Message)
User = SimpleLazyObject(lambda: __import__('django.contrib.auth.models', fromlist=['User']).User)

# Room = lazy_import('room.models', ['Room'])
# Message = lazy_import('room.models', ['Message'])
# User = lazy_import('django.contrib.auth.models', ['User'])
# from room.models import Room ,Message
# from django.contrib.auth.models import User
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" %self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()



    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )    
        
    async def receive(self,text_data):
        data =json.loads(text_data)
        message = data["message"] 
        username = data["username"]
        room = data["room"]

        await self.save_messages(username,room,message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message,
                "username":username,
                "room":room,
            }
        )


    async def chat_message(self,event):
        message= event["message"]
        username= event["username"]
        room= event["room"]

        await self.send(text_data=json.dumps({
            "message":message,
            "username":username,
            "room":room
        }))

    @sync_to_async
    def save_messages(self,username,room,message):
        user = User.objects.get(username= username)
        room =Room.objects.get(slug=room)
        message = Message.objects.create(user =user ,room = room ,content =message)