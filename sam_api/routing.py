from django.urls import re_path
# from sam_api import consumers
from . import consumers

websocket_urlpatterns = [
    # path('ws/entities/', consumers.EntityConsumer.as_asgi()), # This is the old way
    # path('ws/sam_api/', consumers.EntityConsumer.as_asgi()), # This is the old way too
    # re_path(r'ws/entities/$', consumers.EntityConsumer.as_asgi()),
    re_path(r'ws/opportunities/$', consumers.OpportunityConsumer.as_asgi()),
]