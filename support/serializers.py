from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import UserProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    expediteur = UserProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'expediteur', 'date_envoi']

class ConversationSerializer(serializers.ModelSerializer):
    client = UserProfileSerializer(read_only=True)
    agent = UserProfileSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    dernier_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = [
            'id', 'client', 'agent',
            'date_creation', 'date_mise_a_jour'
        ]

    def get_dernier_message(self, obj):
        dernier = obj.messages.last()
        if dernier:
            return MessageSerializer(dernier).data
        return None

class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = []

    def create(self, validated_data):
        client = self.context['request'].user
        return Conversation.objects.create(
            client=client,
            statut='ouverte'
        )

class AssignerAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['agent']
