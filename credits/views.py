from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from datetime import date
from .models import DemandeCredit, Remboursement
from .serializers import (
    DemandeCreditSerializer,
    DemandeCreditCreateSerializer,
    StatutUpdateSerializer,
    RemboursementSerializer,
    EnregistrerPaiementSerializer
)

class DemandeCreditListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Lister mes demandes de crédit")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Soumettre une nouvelle demande de crédit",
        request=DemandeCreditCreateSerializer,
        responses={201: DemandeCreditSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DemandeCreditCreateSerializer
        return DemandeCreditSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return DemandeCredit.objects.filter(client=user)
        return DemandeCredit.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DemandeCreditDetailView(generics.RetrieveAPIView):
    serializer_class = DemandeCreditSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Détail d'une demande de crédit")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return DemandeCredit.objects.filter(client=user)
        return DemandeCredit.objects.all()

class UpdateStatutCreditView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Mettre à jour le statut d'une demande (agent/admin)",
        request=StatutUpdateSerializer,
        responses={200: DemandeCreditSerializer}
    )
    def patch(self, request, pk):
        user = request.user
        if user.role not in ['agent', 'admin']:
            return Response(
                {"error": "Permission refusée."},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            demande = DemandeCredit.objects.get(pk=pk)
        except DemandeCredit.DoesNotExist:
            return Response(
                {"error": "Demande introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = StatutUpdateSerializer(
            demande, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(agent=user)
            return Response(
                DemandeCreditSerializer(demande).data
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class RemboursementListView(generics.ListAPIView):
    serializer_class = RemboursementSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lister les remboursements d'une demande"
    )
    def get_queryset(self):
        demande_id = self.kwargs['demande_id']
        return Remboursement.objects.filter(
            demande_id=demande_id
        )

class EnregistrerPaiementView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Enregistrer un paiement de remboursement",
        request=EnregistrerPaiementSerializer,
        responses={200: RemboursementSerializer}
    )
    def post(self, request, pk):
        user = request.user
        if user.role not in ['agent', 'admin']:
            return Response(
                {"error": "Permission refusée."},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            remboursement = Remboursement.objects.get(pk=pk)
        except Remboursement.DoesNotExist:
            return Response(
                {"error": "Remboursement introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EnregistrerPaiementSerializer(
            data=request.data
        )
        if serializer.is_valid():
            remboursement.montant_paye = (
                serializer.validated_data['montant_paye']
            )
            remboursement.date_paiement = date.today()
            remboursement.statut = 'paye'
            remboursement.enregistre_par = user
            remboursement.save()
            return Response(
                RemboursementSerializer(remboursement).data
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
