from django.contrib import admin
from .models import ProduitAssurance, Souscription

class ProduitAssuranceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_assurance', 'prime_mensuelle', 'duree_mois', 'est_actif']
    list_filter = ['type_assurance', 'est_actif']
    search_fields = ['nom', 'description']

class SouscriptionAdmin(admin.ModelAdmin):
    list_display = ['client', 'produit', 'date_souscription', 'date_expiration', 'statut', 'notification_envoyee']
    list_filter = ['statut', 'date_souscription', 'notification_envoyee']
    search_fields = ['client__username', 'produit__nom']

admin.site.register(ProduitAssurance, ProduitAssuranceAdmin)
admin.site.register(Souscription, SouscriptionAdmin)
