from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EmailStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('email_status', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('email_status', self.channel_name)

    async def status_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
