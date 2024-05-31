import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Opportunity

class EntityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        entities = Opportunity.objects.all().values()
        await self.send(text_data=json.dumps(list(entities)))