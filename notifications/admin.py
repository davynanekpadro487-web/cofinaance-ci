from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'destinataire', 'type_notification', 'est_lu', 'date_creation']
    list_filter = ['type_notification', 'est_lu', 'date_creation']
    search_fields = ['titre', 'message', 'destinataire__username']

admin.site.register(Notification, NotificationAdmin)
