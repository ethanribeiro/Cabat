"""
ASGI config for cabat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
# from socketio import ASGIApp
# import socketio
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from sam_api.consumers import OpportunityConsumer
import sam_api.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cabat.settings')

django_asgi_app = get_asgi_application()

# sio = socketio.AsyncServer(async_mode='asgi')
# socketio_app = ASGIApp(sio)

application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            sam_api.routing.websocket_urlpatterns
        )
    ),
})

# application = get_asgi_application()
