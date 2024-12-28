# support/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # الانضمام إلى مجموعة الغرفة
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # قبول الاتصال WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة المجموعة عند قطع الاتصال
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # تلقي الرسائل من WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # إرسال الرسالة إلى مجموعة الغرفة
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # تلقي الرسائل من مجموعة الغرفة
    async def chat_message(self, event):
        message = event['message']

        # إرسال الرسالة إلى WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
