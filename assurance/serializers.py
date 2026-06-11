from rest_framework import serializers
from datetime import date, timedelta
from .models import ProduitAssurance, Souscription
from accounts.serializers import UserProfileSerializer

class ProduitAssuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitAssurance
        fields = '__all__'

class SouscriptionSerializer(serializers.ModelSerializer):
    client = UserProfileSerializer(read_only=True)
    produit = ProduitAssuranceSerializer(read_only=True)

    class Meta:
        model = Souscription
        fields = '__all__'
        read_only_fields = [
            'id', 'client', 'date_souscription',
            'date_expiration', 'statut'
        ]

class SouscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Souscription
        fields = ['produit']

    def create(self, validated_data):
        client = self.context['request'].user
        produit = validated_data['produit']
        date_expiration = date.today() + timedelta(
            days=30 * produit.duree_mois
        )
        return Souscription.objects.create(
            client=client,
            produit=produit,
            date_expiration=date_expiration,
            statut='active'
        )
