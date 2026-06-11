from rest_framework import serializers
from .models import DemandeCredit, Remboursement
from accounts.serializers import UserProfileSerializer

class RemboursementSerializer(serializers.ModelSerializer):
    enregistre_par = UserProfileSerializer(read_only=True)

    class Meta:
        model = Remboursement
        fields = '__all__'
        read_only_fields = [
            'id', 'penalite', 'date_paiement', 'enregistre_par'
        ]

class DemandeCreditSerializer(serializers.ModelSerializer):
    client = UserProfileSerializer(read_only=True)
    agent = UserProfileSerializer(read_only=True)
    remboursements = RemboursementSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = DemandeCredit
        fields = '__all__'
        read_only_fields = [
            'id', 'client', 'agent', 'statut',
            'score_eligibilite', 'date_soumission',
            'date_mise_a_jour'
        ]

class DemandeCreditCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeCredit
        fields = [
            'montant_demande', 'duree_mois',
            'motif', 'piece_justificative'
        ]

    def validate_montant_demande(self, value):
        if value < 10000:
            raise serializers.ValidationError(
                "Le montant minimum est de 10 000 FCFA."
            )
        if value > 5000000:
            raise serializers.ValidationError(
                "Le montant maximum est de 5 000 000 FCFA."
            )
        return value

    def validate_duree_mois(self, value):
        if value < 1 or value > 24:
            raise serializers.ValidationError(
                "La durée doit être entre 1 et 24 mois."
            )
        return value

    def create(self, validated_data):
        client = self.context['request'].user
        montant = validated_data['montant_demande']
        duree = validated_data['duree_mois']

        # Score d'éligibilité simplifié
        score = 50
        if montant <= 100000:
            score += 20
        elif montant <= 500000:
            score += 10
        if duree <= 6:
            score += 15
        elif duree <= 12:
            score += 10

        demande = DemandeCredit.objects.create(
            client=client,
            score_eligibilite=score,
            **validated_data
        )

        # Générer l'échéancier de remboursement
        taux_interet = 0.02  # 2% par mois
        montant_mensuel = round(
            montant * (1 + taux_interet * duree) / duree, 2
        )
        from datetime import date, timedelta
        date_debut = date.today()
        for i in range(1, duree + 1):
            date_echeance = date_debut + timedelta(days=30 * i)
            Remboursement.objects.create(
                demande=demande,
                numero_echeance=i,
                montant_du=montant_mensuel,
                date_echeance=date_echeance
            )
        return demande

class StatutUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeCredit
        fields = ['statut']

    def validate_statut(self, value):
        statuts_valides = [
            'soumise', 'en_analyse', 'approuvee',
            'decaissee', 'rejetee'
        ]
        if value not in statuts_valides:
            raise serializers.ValidationError("Statut invalide.")
        return value

class EnregistrerPaiementSerializer(serializers.Serializer):
    montant_paye = serializers.DecimalField(
        max_digits=12, decimal_places=2
    )
