import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    @classmethod
    def as_alive_instance(cls, **kwargs):
        return cls.as_asgi(**kwargs)

    async def connect(self):
        self.conversation_id = self.scope[
            'url_route'
        ]['kwargs']['conversation_id']
        self.room_group_name = (
            f'chat_{self.conversation_id}'
        )

        # Récupère le token depuis la query string de l'URL
        from urllib.parse import parse_qs
        from rest_framework_simplejwt.tokens import AccessToken
        from django.contrib.auth import get_user_model

        query_string = self.scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token_list = params.get('token', [])

        if not token_list:
            await self.close()
            return

        try:
            # Décode le token avec AccessToken
            token_payload = AccessToken(token_list[0])
            # Récupère l'user
            User = get_user_model()
            self.user = await database_sync_to_async(User.objects.get)(id=token_payload['user_id'])
        except Exception:
            await self.close()
            return

        await self.accept()

        # Rejoindre le groupe de la conversation
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Marquer l'utilisateur comme en ligne
        await self.set_user_online(
            self.user.id, True
        )

        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': 'Connecté à la conversation '
                       f'{self.conversation_id}'
        }))

    async def disconnect(self, close_code):
        # Quitter le groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Marquer l'utilisateur comme hors ligne
        if hasattr(self, 'user') and self.user and self.user.is_authenticated:
            await self.set_user_online(
                self.user.id, False
            )

    async def receive(self, text_data):
        print(f"Message reçu: {text_data} de {self.user}")
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'message')

            if message_type == 'typing':
                # Indicateur de frappe
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_indicator',
                        'user': self.user.username,
                        'is_typing': data.get('is_typing', False)
                    }
                )
            else:
                # Message normal
                contenu = data.get('message', '')
                if not contenu:
                    return

                # Sauvegarder en base de données
                message = await self.save_message(
                    conversation_id=self.conversation_id,
                    user=self.user,
                    contenu=contenu
                )

                # Diffuser à tout le groupe
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': contenu,
                        'user': self.user.username,
                        'user_id': self.user.id,
                        'role': self.user.role,
                        'message_id': message.id,
                        'date_envoi': str(message.date_envoi)
                    }
                )
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'user': event['user'],
            'user_id': event['user_id'],
            'role': event['role'],
            'message_id': event['message_id'],
            'date_envoi': event['date_envoi']
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
            'is_typing': event['is_typing']
        }))

    @database_sync_to_async
    def save_message(self, conversation_id, user, contenu):
        from .models import Conversation, Message
        conversation = Conversation.objects.get(
            id=conversation_id
        )
        return Message.objects.create(
            conversation=conversation,
            expediteur=user,
            contenu=contenu
        )

    @database_sync_to_async
    def set_user_online(self, user_id, status):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.filter(id=user_id).update(
            is_online=status
        )
