from django.db import models

class ProduitAssurance(models.Model):
    TYPE_CHOICES = [
        ('vie', 'Assurance Vie'),
        ('deces_invalidite', 'Décès-Invalidité'),
    ]
    nom = models.CharField(max_length=200)
    type_assurance = models.CharField(
        max_length=20, choices=TYPE_CHOICES
    )
    description = models.TextField()
    prime_mensuelle = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    duree_mois = models.PositiveIntegerField()
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Souscription(models.Model):
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('expiree', 'Expirée'),
        ('resiliee', 'Résiliée'),
    ]
    client = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='souscriptions'
    )
    produit = models.ForeignKey(
        ProduitAssurance, on_delete=models.CASCADE,
        related_name='souscriptions'
    )
    date_souscription = models.DateField(auto_now_add=True)
    date_expiration = models.DateField()
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='active'
    )
    notification_envoyee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client} - {self.produit} - {self.statut}"
