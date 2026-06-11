from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('agent', 'Agent de terrain'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='client'
    )
    telephone = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    photo_profil = models.ImageField(
        upload_to='profils/', null=True, blank=True
    )
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
