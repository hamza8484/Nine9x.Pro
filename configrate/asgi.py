# config/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from support.routing import websocket_urlpatterns  # استيراد المسارات من support/routing.py

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # إعداد HTTP التقليدي
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # توجيه WebSocket إلى المسارات التي حددتها
    ),
})
