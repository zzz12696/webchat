from channels.generic.websocket import AsyncWebsocketConsumer
import json
import time


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # 加入聊天室向组内所有人广播
        message = '{0} 已加入聊天室...'.format(self.user_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        self.user_name = self.scope['url_route']['kwargs']['user_name']

        # 退出聊天室向组内所有人广播
        message = '{0} 已退出聊天室...'.format(self.user_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = '\n\t\t\t\t\t\t{0}\n{1}'.format(time.ctime(), event['message'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
