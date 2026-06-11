from django.contrib import admin
from .models import Conversation, Message

class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'agent', 'statut', 'date_creation', 'date_mise_a_jour']
    list_filter = ['statut', 'date_creation']
    search_fields = ['client__username', 'agent__username']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'expediteur', 'date_envoi', 'est_lu']
    list_filter = ['est_lu', 'date_envoi']
    search_fields = ['expediteur__username', 'contenu']

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
