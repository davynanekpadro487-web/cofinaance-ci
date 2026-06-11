from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from credits.models import DemandeCredit, Remboursement
from assurance.models import ProduitAssurance, Souscription
from support.models import Conversation, Message
from notifications.models import Notification
from datetime import date, timedelta
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de démo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Création des données de démo...')

        # Nettoyer la base
        Message.objects.all().delete()
        Conversation.objects.all().delete()
        Notification.objects.all().delete()
        Souscription.objects.all().delete()
        Remboursement.objects.all().delete()
        DemandeCredit.objects.all().delete()
        User.objects.filter(
            username__in=[
                'client1','client2','client3',
                'agent1','agent2'
            ]
        ).delete()

        # Créer les utilisateurs
        client1 = User.objects.create_user(
            username='client1',
            email='client1@cofinci.ci',
            password='Client@2026',
            role='client',
            telephone='0701020304',
            region='Abidjan'
        )
        client2 = User.objects.create_user(
            username='client2',
            email='client2@cofinci.ci',
            password='Client@2026',
            role='client',
            telephone='0705060708',
            region='Bouaké'
        )
        client3 = User.objects.create_user(
            username='client3',
            email='client3@cofinci.ci',
            password='Client@2026',
            role='client',
            telephone='0709101112',
            region='San-Pédro'
        )
        agent1 = User.objects.create_user(
            username='agent1',
            email='agent1@cofinci.ci',
            password='Agent@2026',
            role='agent',
            telephone='0720304050',
            region='Abidjan'
        )
        agent2 = User.objects.create_user(
            username='agent2',
            email='agent2@cofinci.ci',
            password='Agent@2026',
            role='agent',
            telephone='0760708090',
            region='Bouaké'
        )

        # Créer les produits d'assurance
        produit1 = ProduitAssurance.objects.create(
            nom='Assurance Vie Essentielle',
            type_assurance='vie',
            description='Couverture vie de base pour '
                        'micro-entrepreneurs.',
            prime_mensuelle=Decimal('2500.00'),
            duree_mois=12,
            est_actif=True
        )
        produit2 = ProduitAssurance.objects.create(
            nom='Assurance Décès-Invalidité Plus',
            type_assurance='deces_invalidite',
            description='Protection complète décès '
                        'et invalidité.',
            prime_mensuelle=Decimal('5000.00'),
            duree_mois=6,
            est_actif=True
        )

        # Créer les demandes de crédit
        demande1 = DemandeCredit.objects.create(
            client=client1,
            agent=agent1,
            montant_demande=Decimal('150000.00'),
            duree_mois=6,
            motif='Achat de stock pour ma boutique de tissus.',
            statut='approuvee',
            score_eligibilite=75
        )
        demande2 = DemandeCredit.objects.create(
            client=client2,
            montant_demande=Decimal('300000.00'),
            duree_mois=12,
            motif='Extension de mon activité de restauration.',
            statut='en_analyse',
            score_eligibilite=60
        )
        demande3 = DemandeCredit.objects.create(
            client=client3,
            montant_demande=Decimal('75000.00'),
            duree_mois=3,
            motif='Achat de matériel agricole.',
            statut='soumise',
            score_eligibilite=55
        )
        demande4 = DemandeCredit.objects.create(
            client=client1,
            agent=agent1,
            montant_demande=Decimal('500000.00'),
            duree_mois=24,
            motif='Création d\'un atelier de couture.',
            statut='decaissee',
            score_eligibilite=80
        )

        # Créer les remboursements pour demande1
        montant_mensuel = Decimal('26500.00')
        for i in range(1, 7):
            statut = 'paye' if i <= 2 else 'en_attente'
            Remboursement.objects.create(
                demande=demande1,
                numero_echeance=i,
                montant_du=montant_mensuel,
                montant_paye=montant_mensuel if i <= 2
                             else Decimal('0'),
                date_echeance=date.today() + timedelta(
                    days=30 * i
                ),
                date_paiement=date.today() if i <= 2 else None,
                statut=statut,
                enregistre_par=agent1 if i <= 2 else None
            )

        # Créer les souscriptions
        Souscription.objects.create(
            client=client1,
            produit=produit1,
            date_expiration=date.today() + timedelta(days=365),
            statut='active'
        )
        Souscription.objects.create(
            client=client2,
            produit=produit2,
            date_expiration=date.today() + timedelta(days=10),
            statut='active'
        )

        # Créer les conversations de support
        conv1 = Conversation.objects.create(
            client=client1,
            agent=agent1,
            statut='en_cours'
        )
        Message.objects.create(
            conversation=conv1,
            expediteur=client1,
            contenu='Bonjour, j\'ai une question sur '
                    'mon remboursement du mois prochain.'
        )
        Message.objects.create(
            conversation=conv1,
            expediteur=agent1,
            contenu='Bonjour ! Je suis là pour vous aider. '
                    'Quelle est votre question ?'
        )
        Message.objects.create(
            conversation=conv1,
            expediteur=client1,
            contenu='Est-ce que je peux décaler '
                    'l\'échéance de 5 jours ?'
        )

        conv2 = Conversation.objects.create(
            client=client2,
            statut='ouverte'
        )
        Message.objects.create(
            conversation=conv2,
            expediteur=client2,
            contenu='Bonsoir, je voudrais des informations '
                    'sur les produits d\'assurance.'
        )

        # Créer les notifications
        Notification.objects.create(
            destinataire=client1,
            titre='Demande de crédit approuvée',
            message='Votre demande de crédit de 150 000 FCFA '
                    'a été approuvée.',
            type_notification='credit'
        )
        Notification.objects.create(
            destinataire=client1,
            titre='Échéance dans 3 jours',
            message='Votre remboursement de 26 500 FCFA '
                    'est dû dans 3 jours.',
            type_notification='remboursement'
        )
        Notification.objects.create(
            destinataire=client2,
            titre='Assurance bientôt expirée',
            message='Votre assurance Décès-Invalidité Plus '
                    'expire dans 10 jours.',
            type_notification='assurance'
        )
        Notification.objects.create(
            destinataire=client2,
            titre='Dossier en cours d\'analyse',
            message='Votre demande de 300 000 FCFA '
                    'est en cours d\'analyse.',
            type_notification='credit'
        )

        self.stdout.write(
            self.style.SUCCESS(
                '\n✅ Données de démo créées avec succès !\n'
                '👤 Comptes disponibles :\n'
                '   Admin   → admin / Admin@2026\n'
                '   Agent 1 → agent1 / Agent@2026\n'
                '   Agent 2 → agent2 / Agent@2026\n'
                '   Client 1 → client1 / Client@2026\n'
                '   Client 2 → client2 / Client@2026\n'
                '   Client 3 → client3 / Client@2026\n'
            )
        )
