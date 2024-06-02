# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Opportunity

# class EntityConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
    
#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         entities = Opportunity.objects.all().values()
#         await self.send(text_data=json.dumps(list(entities)))

import json
from channels.generic.websocket import AsyncWebsocketConsumer
# import socketio

# class EntityConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("entities", self.channel_name)
#         await self.accept()
    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("entities", self.channel_name)
    
#     async def receive(self, text_data):
#         await self.channel_layer.group_send("entities", {
#             "type": "send_entities", "text": text_data}
#         )
    
#     async def send_entities(self, event):
#         await self.send(text_data=json.dumps(event["text"]))

# sio = socketio.AsyncServer(async_mode='asgi')

# class OpportunityConsumer(socketio.AsyncNamespace):
#     def on_connect(self, sid, environ):
#         print(f"Connected: {sid}")
    
#     def on_disconnect(self, sid):
#         print(f"Client disconnected: {sid}")
    
#     def on_message(self, sid, data):
#         print(f"Message from cliet: {data}")
#         self.send(sid, data)

# sio.register_namespace(OpportunityConsumer('/ws/opportunities/'))

class OpportunityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("opportunity_updates", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("opportunity_updates", self.channel_name)
    
    async def receive(self, text_data):
        pass
    
    async def opportunity_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            'message': message
        }))