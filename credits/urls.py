from django.urls import path
from .views import (
    DemandeCreditListCreateView,
    DemandeCreditDetailView,
    UpdateStatutCreditView,
    RemboursementListView,
    EnregistrerPaiementView
)

urlpatterns = [
    path('', DemandeCreditListCreateView.as_view(),
         name='credits_list'),
    path('<int:pk>/', DemandeCreditDetailView.as_view(),
         name='credit_detail'),
    path('<int:pk>/statut/', UpdateStatutCreditView.as_view(),
         name='update_statut'),
    path('<int:demande_id>/remboursements/',
         RemboursementListView.as_view(),
         name='remboursements_list'),
    path('remboursements/<int:pk>/payer/',
         EnregistrerPaiementView.as_view(),
         name='enregistrer_paiement'),
]
