# Documentation Complète de l'Application Flask

![Dependencies](https://img.shields.io/librariesio/release/pypi/flask)
![GitHub Release](https://img.shields.io/github/v/release/username/repo?include_prereleases)
![Custom Badge](https://img.shields.io/badge/{{label}}-{{message}}-{{color}}?logo=flask)
![SQLAlchemy](https://img.shields.io/pypi/v/sqlalchemy?label=SQLAlchemy)
![Flask Version](https://img.shields.io/github/pipenv/locked/dependency-version/username/repo/flask?color=green)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green?logo=flask)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blueviolet?logo=postgresql)
![JWT](https://img.shields.io/badge/JWT-v4.4.2-yellow)

![CI](https://github.com/username/repo/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/username/repo)
![License](https://img.shields.io/github/license/username/repo)

## Table des Matières
1. [Introduction](#introduction)
2. [Structure du Projet](#structure-du-projet)
3. [Configuration Initiale](#configuration-initiale)
4. [Modèles de Données](#modèles-de-données)
5. [Routes et Authentification](#routes-et-authentification)
6. [Sécurité et Permissions](#sécurité-et-permissions)
7. [Déploiement](#déploiement)
8. [FAQ](#faq)

---

## Introduction

Cette application Flask est une API REST sécurisée avec système d'authentification et gestion des permissions. Elle inclut :
- Authentification JWT (JSON Web Tokens)
- Gestion des utilisateurs, rôles et permissions
- Validation des données
- Gestion centralisée des erreurs
- Sécurité avancée (CORS, rate limiting)

---

## Structure du Projet

```
flask_app/
├── app/                  # Code principal de l'application
│   ├── __init__.py       # Initialisation de l'app et configuration
│   ├── config.py         # Configuration de l'application
│   ├── models/           # Modèles de base de données
│   ├── routes/           # Routes API
│   ├── schemas/          # Schémas de validation
│   └── utils/            # Utilitaires
├── run.py                # Point d'entrée
├── requirements.txt      # Dépendances Python
├── .env                  # Variables d'environnement
└── README.md             # Documentation
```

---

## Configuration Initiale

### Prérequis
- Python 3.8+
- PostgreSQL (ou autre base de données SQL)
- pip

### Installation
1. Cloner le dépôt
2. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Créer un fichier `.env` à la racine :
   ```ini
   SECRET_KEY=votre_cle_secrete
   JWT_SECRET_KEY=votre_cle_jwt
   DATABASE_URI=postgresql://user:password@localhost/dbname
   ```

2. Configurer la base de données :
   ```python
   # Dans app/__init__.py après db.init_app(app)
   with app.app_context():
       db.create_all()
       # Créer des rôles/permissions initiaux si nécessaire
   ```

---

## Modèles de Données

### User
- `id`: Identifiant unique
- `username`: Nom d'utilisateur
- `password`: Mot de passe hashé
- `email`: Email
- `role_id`: Référence au rôle

### Role
- `id`: Identifiant unique
- `name`: Nom du rôle (admin, client, etc.)
- `permissions`: Liste des permissions associées

### Permission
- `id`: Identifiant unique
- `name`: Nom de la permission (manage_users, etc.)

### Relation Role-Permission
Table de jointure many-to-many entre rôles et permissions.

---

## Routes et Authentification

### Authentification
- **POST /api/auth/register** : Enregistrement d'un nouvel utilisateur
  ```json
  {
    "username": "test",
    "password": "test123",
    "name": "Test User",
    "email": "test@example.com",
    "role": "client"
  }
  ```

- **POST /api/auth/login** : Connexion
  ```json
  {
    "username": "test",
    "password": "test123"
  }
  ```
  Retourne des cookies JWT

- **POST /api/auth/refresh** : Rafraîchir le token
- **POST /api/auth/logout** : Déconnexion

### Utilisateurs
- **GET /api/users/** : Liste des utilisateurs (nécessite permission `manage_users`)

---

## Sécurité et Permissions

### JWT Configuration
- Tokens stockés dans des cookies HTTP-only
- Protection CSRF avec SameSite=Lax
- Expiration : 15 minutes (access), 30 jours (refresh)

### Décorateurs de Sécurité
```python
@permission_required("manage_users")
def get_users():
    # Nécessite la permission manage_users
```

### Rate Limiting
Limite automatique les requêtes pour prévenir les attaques par force brute.

---

## Déploiement

### Production
1. Changer en `.env` :
   ```ini
   JWT_COOKIE_SECURE=True
   ```
2. Utiliser un serveur WSGI comme Gunicorn :
   ```bash
   gunicorn -w 4 run:app
   ```

### Docker (Exemple)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "4", "run:app"]
```

---

## FAQ

**Q: Comment ajouter une nouvelle permission?**
1. Ajouter une entrée dans la table Permission
2. Associer à un rôle via RolePermission
3. Utiliser le décorateur `@permission_required`

**Q: Problèmes de CORS?**
Vérifier la configuration dans `app/__init__.py` et s'assurer que le front-end envoie les credentials.

**Q: Comment tester l'API?**
Utiliser Postman ou curl avec les options `-c cookies.txt -b cookies.txt` pour gérer les sessions.

---

## Bonnes Pratiques

1. **Ne jamais** commiter le fichier `.env`
2. Toujours utiliser HTTPS en production
3. Mettre à jour régulièrement les dépendances
4. Implémenter des tests unitaires supplémentaires