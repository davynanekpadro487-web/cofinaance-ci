from django.db import models

class Notification(models.Model):
    TYPE_CHOICES = [
        ('credit', 'Crédit'),
        ('remboursement', 'Remboursement'),
        ('assurance', 'Assurance'),
        ('support', 'Support'),
    ]
    destinataire = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='notifications'
    )
    titre = models.CharField(max_length=255)
    message = models.TextField()
    type_notification = models.CharField(
        max_length=20, choices=TYPE_CHOICES
    )
    est_lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} → {self.destinataire}"
