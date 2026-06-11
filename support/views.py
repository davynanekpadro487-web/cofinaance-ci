from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    AssignerAgentSerializer
)

class ConversationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Lister mes conversations de support")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Ouvrir une nouvelle conversation de support",
        request=ConversationCreateSerializer,
        responses={201: ConversationSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Conversation.objects.filter(client=user)
        return Conversation.objects.all()

class ConversationDetailView(generics.RetrieveAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Détail d'une conversation avec historique"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Conversation.objects.filter(client=user)
        return Conversation.objects.all()

class AssignerAgentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Assigner un agent à une conversation (admin)",
        request=AssignerAgentSerializer,
        responses={200: ConversationSerializer}
    )
    def patch(self, request, pk):
        user = request.user
        if user.role not in ['agent', 'admin']:
            return Response(
                {"error": "Permission refusée."},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        conversation.agent = user
        conversation.statut = 'en_cours'
        conversation.save()
        return Response(
            ConversationSerializer(conversation).data
        )

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lister les messages d'une conversation"
    )
    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(
            conversation_id=conversation_id
        )
