from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from users.consumers import SocketConsumer
application = ProtocolTypeRouter({
    'users': URLRouter([
        path('ws/users/', SocketConsumer.as_asgi()),
    ])
})
