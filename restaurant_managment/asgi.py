# restaurant_managment/asgi.py

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from support.routing import websocket_urlpatterns
from support import consumers  # تأكد من أن ملف consumers موجود في تطبيق support

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_managment.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # يمرر طلبات HTTP التقليدية
    "websocket": AuthMiddlewareStack(  # يمرر طلبات WebSocket
        URLRouter([
            path('ws/chat/', consumers.ChatConsumer.as_asgi()),  # تحديد المسار الخاص بـ WebSocket
        ])
    ),
})

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
