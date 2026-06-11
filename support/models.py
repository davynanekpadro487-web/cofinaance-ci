from django.db import models

class Conversation(models.Model):
    STATUT_CHOICES = [
        ('ouverte', 'Ouverte'),
        ('en_cours', 'En cours'),
        ('fermee', 'Fermée'),
    ]
    client = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE,
        related_name='conversations'
    )
    agent = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='conversations_traitees'
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='ouverte'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.client}"

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE,
        related_name='messages'
    )
    expediteur = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE
    )
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_envoi']

    def __str__(self):
        return f"Message de {self.expediteur} - {self.date_envoi}"
