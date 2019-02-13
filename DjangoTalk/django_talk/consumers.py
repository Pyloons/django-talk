from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from .models import ChatRoom
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope['user'].is_authenticated():
            self.accept()
            # Join room group
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name.replace(' ','')
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name)

            # Send message to room group
            this_room = ChatRoom.objects.get(channel_name=self.room_name)
            this_room.members.add(self.scope['user'])
            this_room.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'users_change',
                }
            )
        else:
            self.close()


    def disconnect(self, close_code):
        if self.scope['user'].is_authenticated():
            this_room = ChatRoom.objects.get(channel_name=self.room_name)
            this_room.members.remove(self.scope['user'])
            this_room.save()
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'users_change',
                }
            )
            # Leave room group
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        else:
            pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = self.scope['user'].username
        time = datetime.now()
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': username if username != '' else '未登录用户',
                'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        username = event['username']
        time = event['time']
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'hasMessage': True,
            'username': username if username != '' else '未登录用户',
            'time': time,
            'message': message
        }))

    def users_change(self, event):
        members = ChatRoom.objects.get(channel_name=self.room_name).members.get_queryset()
        members_name = [member.username for member in members]
        self.send(text_data=json.dumps({
            'userChange': True,
            'members': members_name
        }))
