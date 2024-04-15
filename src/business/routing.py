from django.urls import re_path, path
from .consumers import BusinessSocketConsumer
from chat.consumers import ChatConsumer

websocket_patterns = [
    path(r'chat/<str:user_id>/', ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    path(r'ws/eprofile/<str:user_id>/', BusinessSocketConsumer.as_asgi())
]