# COFINANCE CI — Plateforme Digitale de Microfinance

Plateforme de gestion de microcrédits, d'assurance mobile
et de support client en temps réel.
Développée avec Django 5.1 et Django REST Framework.

---

## Prérequis

- Python 3.11+
- pip
- Git

---

## Installation

### 1. Cloner le dépôt

git clone https://github.com/cofinci/cofinci.git
cd cofinci

### 2. Créer et activer l'environnement virtuel

# Windows
python -m venv env
env\Scripts\activate

# Mac/Linux
python -m venv env
source env/bin/activate

### 3. Installer les dépendances

pip install -r requirements.txt

### 4. Appliquer les migrations

python manage.py migrate

### 5. Peupler la base de données de démo

python manage.py seed_db

### 6. Lancer le serveur

# Avec Daphne (WebSocket activé) :
daphne -p 8000 cofinci.asgi:application

# Ou avec Django standard (sans WebSocket) :
python manage.py runserver

---

## Accès à l'application

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/api/docs/ | Documentation Swagger |
| http://127.0.0.1:8000/admin/ | Interface d'administration |
| http://127.0.0.1:8000/chat/ | Interface de chat en temps réel |

---

## Comptes de démonstration

| Rôle | Username | Mot de passe |
|------|----------|--------------|
| Administrateur | admin | Admin@2026 |
| Agent | agent1 | Agent@2026 |
| Agent | agent2 | Agent@2026 |
| Client | client1 | Client@2026 |
| Client | client2 | Client@2026 |
| Client | client3 | Client@2026 |

---

## Modules de l'API

| Module | Endpoint de base |
|--------|-----------------|
| Authentification | /api/accounts/ |
| Microcrédits | /api/credits/ |
| Assurance mobile | /api/assurance/ |
| Notifications | /api/notifications/ |
| Support chat | /api/support/ |
| Tableau de bord | /api/dashboard/ |

---

## Démonstration du chat en temps réel

1. Lancer le serveur avec Daphne
2. Ouvrir http://127.0.0.1:8000/chat/ 
   dans deux onglets différents
3. Dans le premier onglet : se connecter avec 
   le token JWT de client1
4. Dans le second onglet : se connecter avec 
   le token JWT de agent1
5. Les deux utilisateurs voient les messages 
   en temps réel

Pour obtenir un token JWT :
POST /api/accounts/login/
{
  "username": "client1",
  "password": "Client@2026"
}

---

## Stack technique

- Backend : Python 3.11, Django 5.1
- API : Django REST Framework 3.15
- Auth : JWT via djangorestframework-simplejwt
- WebSocket : Django Channels 4.1 + Daphne
- Documentation : drf-spectacular (Swagger)
- Base de données : SQLite (dev) / PostgreSQL (prod)
