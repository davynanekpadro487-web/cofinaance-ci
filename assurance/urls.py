from django.urls import path
from .views import (
    ProduitAssuranceListView,
    SouscriptionListCreateView,
    SouscriptionDetailView
)

urlpatterns = [
    path('produits/', ProduitAssuranceListView.as_view(),
         name='produits_list'),
    path('souscriptions/', SouscriptionListCreateView.as_view(),
         name='souscriptions_list'),
    path('souscriptions/<int:pk>/',
         SouscriptionDetailView.as_view(),
         name='souscription_detail'),
]
