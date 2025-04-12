import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashBoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("log_group", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("log_group", self.channel_name)

    async def send_log(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()

