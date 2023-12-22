import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from your_app.consumers import ChatRoomConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<ecommerce>.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                [
                    path('ws/some_path/<ChatRoomConsumer>/', ChatRoomConsumer.as_asgi()),
                ]
            )
        ),
    }
)
