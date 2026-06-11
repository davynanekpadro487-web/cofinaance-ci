from django.contrib import admin
from .models import DemandeCredit, Remboursement

class DemandeCreditAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'agent', 'montant_demande', 'duree_mois', 'statut', 'score_eligibilite', 'date_soumission']
    list_filter = ['statut', 'date_soumission']
    search_fields = ['client__username', 'agent__username', 'motif']

class RemboursementAdmin(admin.ModelAdmin):
    list_display = ['id', 'demande', 'numero_echeance', 'montant_du', 'montant_paye', 'penalite', 'date_echeance', 'statut']
    list_filter = ['statut', 'date_echeance']
    search_fields = ['demande__client__username']

admin.site.register(DemandeCredit, DemandeCreditAdmin)
admin.site.register(Remboursement, RemboursementAdmin)
