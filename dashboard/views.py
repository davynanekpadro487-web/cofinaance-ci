from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from credits.models import DemandeCredit, Remboursement
from assurance.models import Souscription
from support.models import Conversation
from accounts.models import User

class TableauDeBordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Tableau de bord administrateur — indicateurs clés"
    )
    def get(self, request):
        user = request.user
        if user.role != 'admin':
            return Response(
                {"error": "Réservé aux administrateurs."},
                status=403
            )

        # Indicateurs crédits
        credits_par_statut = {}
        for statut, _ in DemandeCredit.STATUT_CHOICES:
            credits_par_statut[statut] = (
                DemandeCredit.objects.filter(statut=statut).count()
            )

        # Taux de recouvrement
        total_du = sum(
            r.montant_du for r in Remboursement.objects.all()
        )
        total_paye = sum(
            r.montant_paye for r in Remboursement.objects.all()
        )
        taux_recouvrement = (
            round((float(total_paye) / float(total_du)) * 100, 2)
            if total_du > 0 else 0
        )

        # Assurances
        souscriptions_actives = Souscription.objects.filter(
            statut='active'
        ).count()

        # Support
        conversations_ouvertes = Conversation.objects.filter(
            statut__in=['ouverte', 'en_cours']
        ).count()

        # Utilisateurs
        total_clients = User.objects.filter(
            role='client'
        ).count()
        total_agents = User.objects.filter(
            role='agent'
        ).count()

        return Response({
            "credits": {
                "par_statut": credits_par_statut,
                "total": DemandeCredit.objects.count(),
            },
            "remboursements": {
                "taux_recouvrement_pct": taux_recouvrement,
                "total_du_fcfa": float(total_du),
                "total_paye_fcfa": float(total_paye),
            },
            "assurance": {
                "souscriptions_actives": souscriptions_actives,
            },
            "support": {
                "conversations_ouvertes": conversations_ouvertes,
            },
            "utilisateurs": {
                "total_clients": total_clients,
                "total_agents": total_agents,
            }
        })
