from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import ProduitAssurance, Souscription
from .serializers import (
    ProduitAssuranceSerializer,
    SouscriptionSerializer,
    SouscriptionCreateSerializer
)

class ProduitAssuranceListView(generics.ListAPIView):
    serializer_class = ProduitAssuranceSerializer
    permission_classes = [IsAuthenticated]
    queryset = ProduitAssurance.objects.filter(est_actif=True)

    @extend_schema(
        summary="Lister les produits d'assurance disponibles"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SouscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Lister mes souscriptions actives")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Souscrire à un produit d'assurance",
        request=SouscriptionCreateSerializer,
        responses={201: SouscriptionSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SouscriptionCreateSerializer
        return SouscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Souscription.objects.filter(client=user)
        return Souscription.objects.all()

class SouscriptionDetailView(generics.RetrieveAPIView):
    serializer_class = SouscriptionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Détail d'une souscription")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Souscription.objects.filter(client=user)
        return Souscription.objects.all()
