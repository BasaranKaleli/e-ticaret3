from channels.generic.websocket import AsyncWebsocketConsumer
from email.message import EmailMessage
from django.core.mail import get_connection, send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from page.views import STATUS
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

class EmailConsumerMixin:
    async def send_email(self, subject, message, from_email, recipient_list):
        # E-posta gönderen ve alıcı bilgilerini ayarla
        sender_email = "gonderen@example.com"
        recipient_email = "alici@example.com"

        # E-posta başlığı ve içeriği
        subject = "Sipariş Onayı"
        body = f"Siparişiniz onaylanmıştır. Sipariş Detayları:\n\n{order_data}"

        # E-posta mesajını oluştur
        email_message = EmailMessage(
            subject,
            body,
            sender_email,
            [recipient_email],
        )

        # E-posta gönderimini başlat
        connection = get_connection(backend='django.core.mail.backends.smtp.EmailBackend')
        await connection.send_messages([email_message])

        print("E-posta başarıyla gönderildi.")

class CombinedConsumer(AsyncWebsocketConsumer, EmailConsumerMixin):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        order_data = data['order_data']

        # E-posta gönderme işlemini başlat
        await self.send_email("Sipariş Onayı", f"Sipariş Detayları:\n\n{order_data}", "gonderen@example.com", ["alici@example.com"])