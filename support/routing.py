

from django.urls import re_path
from . import consumers  # استيراد الكلاس ChatConsumer

# تحديد المسار الذي سيتم استخدامه للاتصال عبر WebSocket
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),  # مسار WebSocket للدردشة
]
