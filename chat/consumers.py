import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_conversation_{self.conversation_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from .models import Message, Conversation  # Import model bên trong hàm để tránh lỗi AppRegistryNotReady
        data = json.loads(text_data)
        message = data['message']
        user = self.scope["user"]
        conversation = await sync_to_async(Conversation.objects.get)(id=self.conversation_id)
        if user.is_authenticated:
            sender = user.get_full_name() or user.username
            is_admin = user.is_staff
            sender_user = user
        else:
            sender = self.scope["session"].get("guest_name", "Guest")
            is_admin = False
            sender_user = None
        msg = await sync_to_async(Message.objects.create)(
            conversation=conversation,
            sender=sender,
            sender_user=sender_user,
            content=message,
            is_admin=is_admin
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'is_admin': is_admin,
                'timestamp': msg.timestamp.strftime('%H:%M %d/%m/%Y'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'is_admin': event['is_admin'],
            'timestamp': event['timestamp'],
        })) 