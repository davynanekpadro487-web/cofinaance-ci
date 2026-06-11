from django.db import models

class DemandeCredit(models.Model):
    STATUT_CHOICES = [
        ('soumise', 'Soumise'),
        ('en_analyse', 'En analyse'),
        ('approuvee', 'Approuvée'),
        ('decaissee', 'Décaissée'),
        ('rejetee', 'Rejetée'),
    ]
    client = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='demandes_credit'
    )
    agent = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='dossiers_traites'
    )
    montant_demande = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    duree_mois = models.PositiveIntegerField()
    motif = models.TextField()
    piece_justificative = models.FileField(
        upload_to='pieces/', null=True, blank=True
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='soumise'
    )
    score_eligibilite = models.IntegerField(default=0)
    date_soumission = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Crédit {self.id} - {self.client} - {self.statut}"

class Remboursement(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('en_retard', 'En retard'),
    ]
    demande = models.ForeignKey(
        DemandeCredit, on_delete=models.CASCADE,
        related_name='remboursements'
    )
    numero_echeance = models.PositiveIntegerField()
    montant_du = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    montant_paye = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    penalite = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    date_echeance = models.DateField()
    date_paiement = models.DateField(null=True, blank=True)
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='en_attente'
    )
    enregistre_par = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return f"Échéance {self.numero_echeance} - {self.demande}"
