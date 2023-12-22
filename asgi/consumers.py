from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{room_name}"

        # Kullanıcıyı belirli bir odaya ekleyerek takip edebilirsiniz
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Kullanıcının bağlandığını diğer kullanıcılara bildirebilirsiniz
        await self.send_system_message(f"Kullanıcı '{self.scope['user']}' bağlandı.")

        await self.accept()

    async def disconnect(self, close_code):
        # Kullanıcıyı odadan çıkararak takibi sonlandırabilirsiniz
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Kullanıcının ayrıldığını diğer kullanıcılara bildirebilirsiniz
        await self.send_system_message(f"Kullanıcı '{self.scope['user']}' ayrıldı.")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Alınan mesajı belirli bir odaya yayınlayabilirsiniz
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': self.scope['user'],
            }
        )

    async def chat_message(self, event):
        # Odadaki kullanıcılara mesajı yayınlayabilirsiniz
        message = event['message']
        user = event['user']

        # Mesajı alan kullanıcıya özel bir biçimde gönderebilirsiniz
        personalized_message = f"{user}: {message}"
        await self.send(text_data=json.dumps({'message': personalized_message}))

    async def send_system_message(self, message):
        # Sistem mesajlarını tüm kullanıcılara gönderebilirsiniz
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'system.message',
                'message': message,
            }
        )

    async def system_message(self, event):
        # Sistem mesajlarını kullanıcılara gönderebilirsiniz
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
