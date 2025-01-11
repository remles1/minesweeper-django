from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path("ws/game/<difficulty>", consumers.GameConsumer.as_asgi()),
]
