from django.urls import path
from .views import (
    ConversationListCreateView,
    ConversationDetailView,
    AssignerAgentView,
    MessageListView
)

urlpatterns = [
    path('conversations/',
         ConversationListCreateView.as_view(),
         name='conversations_list'),
    path('conversations/<int:pk>/',
         ConversationDetailView.as_view(),
         name='conversation_detail'),
    path('conversations/<int:pk>/assigner/',
         AssignerAgentView.as_view(),
         name='assigner_agent'),
    path('conversations/<int:conversation_id>/messages/',
         MessageListView.as_view(),
         name='messages_list'),
]
