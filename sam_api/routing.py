from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/entities/', consumers.EntityConsumer.as_asgi()),
]