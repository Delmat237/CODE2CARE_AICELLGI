# 🛠️ Patient Feedback and Reminder Backend

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-orange.svg)

> **Backend API pour la gestion des retours patients et rappels à Douala General Hospital**

## 📌 Table of Contents
- [Fonctionnalités](#-fonctionnalités)
    - [Fonctionnalités principales](#fonctionnalités-principales)
    - [*Intégration et API](#intégration-et-api)
- [Architecture du systeme](#-architecture)
- [Arborescence expliquée](#-arborescence-expliquée)
- [ Vue d'Ensemble des Fichiers et Dossiers](#-vue-densemble-des-fichiers-et-dossiers)
- [roadmap](#-prochaines-étapes-dici-le-18-juillet-2025)
- [Mise à jour 1](#-mises-à-jour-14-juillet-2024)
- [Mise à jour 2](#-nouveautés-mise-à-jour-16-juillet-2024)
- [Pile Technologique](#-pile-technologique)
- [Modèle de données](#-modèles-de-données)
- [Setup Guide](#-démarrage)
- [Utilisation](#-utilisation)
- [How to Contribute](#-contribution)


Une API backend robuste et scalable développée avec FastAPI pour collecter les retours patients, gérer les rappels automatisés, et analyser les données dans un environnement multilingue (anglais, français, Douala, Bassa, Ewondo), optimisée pour les zones à faible bande passante.


## 🚀 Fonctionnalités

### **Fonctionnalités principales**
- **Soumission de retours** - Collecte de texte, voix, emojis, et notes par étoiles dans 5 langues.
- **Gestion hors ligne** - Stockage temporaire et synchronisation différée.
- **Analyse des retours** - Intégration avec un moteur NLP (à implémenter).
- **Rappels automatisés** - Envoi via SMS, IVR, ou email avec Twilio et SMTP.

### **Intégration et API**
- **API RESTful** - Endpoints pour soumissions et rappels.
- **Support Twilio** - Intégration SMS/IVR pour les zones sans connexion web.
- **Notifications par email** - Envoi personnalisé via SMTP (ex. SendGrid).
- **Traitement léger** - Optimisation pour faible bande passante (< 256 kbps).
- **Support multi-format** - JSON pour les API.

## 🏗️ Architecture
```
┌────────────────────┐    ┌────────────────────┐
│   API Backend      │    │   Base de données  │
│   (FastAPI)        │◄──►│   (PostgreSQL)     │
└────────────────────┘    └────────────────────┘
        │                        │
        │                        │
        ├────────┐               ▼
        │        │       ┌────────────────────┐
        │        └──────►│   Cache/Queue      │
        │                │   (Redis)          │
        │                └────────────────────┘
        ▼
┌────────────────────┐    ┌────────────────────┐
│   Twilio Services  │    │   Email Service    │
│   (SMS/IVR)        │    │   (SMTP/SendGrid)  │
└────────────────────┘    └────────────────────┘
```

## 🌳 Arborescence expliquée

```
Track1/backend/
│
├── main.py                  # Point d'entrée de l'application FastAPI
├── config/                  # Configuration et variables d'environnement
│   └── settings.py          # Paramètres globaux avec Pydantic BaseSettings
├── database/                # Gestion de la base de données
│   ├── init.py          # Initialisation du module
│   ├── database.py          # Connexion SQLAlchemy et gestion des sessions
│   └── migrations/          # Scripts de migration Alembic
│       ├── env.py           # Configuration de l'environnement de migration
│       ├── script.py.mako   # Modèle de script de migration
│       └── versions/        # Versions de migration générées
├── models/                  # Modèles SQLAlchemy pour la persistance
│   ├── init.py          # Initialisation du module
│   ├── user.py              # Modèle Utilisateur
│   ├── patient.py           # Modèle Patient
│   ├── feedback.py          # Modèle Retour
│   └── reminder.py          # Modèle Rappel
├── schemas/                 # Schémas Pydantic pour la validation
│   ├── init.py          # Initialisation du module
│   ├── user.py              # Schéma Utilisateur
│   ├── patient.py           # Schéma Patient
│   ├── feedback.py          # Schéma Retour
│   └── reminder.py          # Schéma Rappel
├── routers/                 # Définitions des endpoints API
│   ├── init.py          # Initialisation du module
│   ├── auth.py              # Endpoints d'authentification
│   ├── feedback.py          # Endpoints de retours
│   ├── reminders.py         # Endpoints de rappels
│   └── dashboard.py         # Endpoints d'analytique
├── utils/                   # Utilitaires et intégrations externes
│   ├── init.py          # Initialisation du module
│   ├── twilio_client.py     # Intégration Twilio pour SMS/IVR
│   └── email_client.py      # Intégration SMTP pour email
├── tests/                   # Tests unitaires et d'intégration
│   ├── init.py          # Initialisation du module
│   ├── test_auth.py         # Tests d'authentification
│   ├── test_feedback.py     # Tests des endpoints de retours
│   ├── test_reminders.py    # Tests des endpoints de rappels
│   └── integration/         # Tests d'intégration (à développer)
├── alembic.ini              # Configuration principale d'Alembic
├── requirements.txt         # Dépendances Python
├── .env.example             # Exemple de fichier de variables d'environnement
├── docker-compose.yml       # Configuration Docker pour le développement
├── docker-compose.prod.yml  # Configuration Docker pour la production
└── README.md                # Documentation du projet
```


## 📋 Vue d'Ensemble des Fichiers et Dossiers

### **`main.py`**
- **Rôle** : Point d'entrée de l'application FastAPI avec configuration CORS, inclusion des routers, et lancement avec Uvicorn (hôte : `0.0.0.0`, port : `8000`).

### **`config/settings.py`**
- **Rôle** : Gère les configurations avec Pydantic (`DATABASE_URL`, `TWILIO_*`, `SMTP_*`, `SECRET_KEY`, etc.) chargées depuis `.env`.

### **`database/`**
- **database.py** : Gère la connexion à PostgreSQL avec SQLAlchemy et fournit la dépendance `get_db`.
- **migrations/** : Utilise Alembic pour gérer les schémas de la base de données (ex. `users`, `patients`, `feedbacks`, `reminders`).

### **`models/`**
- **user.py** : Modèle SQLAlchemy pour la table `users`.
- **patient.py** : Modèle SQLAlchemy pour la table `patients`.
- **feedback.py** : Modèle SQLAlchemy pour la table `feedbacks`.
- **reminder.py** : Modèle SQLAlchemy pour la table `reminders`.

### **`schemas/`**
- **user.py** : Schéma Pydantic pour la validation des données utilisateur.
- **patient.py** : Schéma Pydantic pour la validation des données patient.
- **feedback.py** : Schéma Pydantic pour la validation des données de retour.
- **reminder.py** : Schéma Pydantic pour la validation des données de rappel.

### **`routers/`**
- **auth.py** : Endpoints pour l'authentification (connexion, inscription, rafraîchissement, déconnexion, profil).
- **feedback.py** : Endpoints pour les opérations CRUD sur les retours.
- **reminders.py** : Endpoints pour les opérations CRUD et la planification des rappels.
- **dashboard.py** : Endpoints pour les analyses administratives.

### **`utils/`**
- **twilio_client.py** : Intègre Twilio pour les notifications SMS et IVR.
- **email_client.py** : Intègre SMTP pour les notifications par email.

### **`tests/`**
- **test_auth.py** : Tests unitaires pour les endpoints d'authentification.
- **test_feedback.py** : Tests unitaires pour les endpoints de retours.
- **test_reminders.py** : Tests unitaires pour les endpoints de rappels.
- **integration/** : Dossier pour les tests d'intégration (à développer).

### **Fichiers de Configuration**
- **alembic.ini** : Configuration principale d'Alembic.
- **requirements.txt** : Liste des dépendances (ex. `fastapi`, `sqlalchemy`, `twilio`, `pydantic`).
- **.env.example** : Modèle de fichier de variables d'environnement avec commentaires.
- **docker-compose.yml** : Définit les services (app, PostgreSQL, Redis) pour le développement.
- **docker-compose.prod.yml** : Définit la configuration de production avec k3s.

## ⚙️ Considérations de Conception

- **Modularité** : Composants isolés (routes, modèles, utilitaires) pour une maintenance facile.
- **Scalabilité** : k3s pour une orchestration légère et Redis pour le cache.
- **Optimisation Faible Bande Passante** : Réponses compressées (Gzip), gestion asynchrone.
- **Sécurité** : Authentification JWT, chiffrement TLS (à configurer), limitation de taux.

## ⏰ Prochaines Étapes (d'ici le 18 juillet 2025)
- Implémenter les tests d'intégration dans `tests/integration/`.
- Ajouter la transcription vocale dans `utils/` avec Google Speech-to-Text.
- Configurer l'authentification JWT dans `main.py` et `routers/`.
- Générer `openapi.json` pour la documentation des endpoints.

## 🚀 Mises à Jour (14 juillet 2024)
### Fonctionnalités Ajoutées
- **Système d'Authentification Complet** : JWT avec tokens d'accès et de rafraîchissement.
- **CRUD Complet** : Pour les retours et rappels.
- **Traitement Vocal Initial** : Intégré avec Google Speech-to-Text.

## 🔐 Authentification

### Endpoints
- `POST /api/auth/login` - Authentification avec nom d'utilisateur/mot de passe.
- `POST /api/auth/register` - Création d'un compte utilisateur.
- `POST /api/auth/refresh` - Rafraîchissement du token d'accès.
- `POST /api/auth/logout` - Invalidation du token de rafraîchissement.
- `GET /api/auth/me` - Récupération des informations utilisateur.

### Sécurité
- Tokens JWT signés avec une clé secrète.
- Tokens de rafraîchissement stockés dans la table `refresh_tokens`.
- Expiration configurable (30 minutes pour le token d'accès, 7 jours pour le token de rafraîchissement).

## 📝 API Retours (CRUD Complet)

### Endpoints
| Méthode | Endpoint            | Description                  |
|---------|---------------------|------------------------------|
| POST    | `/api/feedback`     | Soumettre un nouveau retour  |
| GET     | `/api/feedback`     | Lister tous les retours      |
| GET     | `/api/feedback/{id}`| Récupérer un retour spécifique |
| PUT     | `/api/feedback/{id}`| Mettre à jour un retour      |
| DELETE  | `/api/feedback/{id}`| Supprimer un retour          |

### Fonctionnalités Spéciales
- **Traitement Vocal** : Transcription automatique des enregistrements audio.
- **Traduction** : Conversion des retours en langue locale vers le français.
- **Validation** : Modèles Pydantic stricts pour les entrées/sorties.

## ⏰ API Rappels (CRUD Complet)

### Endpoints
| Méthode | Endpoint            | Description                  |
|---------|---------------------|------------------------------|
| POST    | `/api/reminders`    | Créer un nouveau rappel      |
| GET     | `/api/reminders`    | Lister tous les rappels      |
| GET     | `/api/reminders/{id}`| Récupérer un rappel spécifique |
| PUT     | `/api/reminders/{id}`| Mettre à jour un rappel      |
| DELETE  | `/api/reminders/{id}`| Supprimer un rappel          |

### Fonctionnalités Spéciales
- **Planification Flexible** : Dates et heures configurables.
- **Multi-Canal** : Envoi par SMS, IVR ou email.
- **Statut de Livraison** : Suivi de l'état des rappels (en attente, envoyé, échoué).

## 👤 API Gestion des Patients (CRUD Complet)

### Endpoints
| Méthode | Endpoint            | Description                  |
|---------|---------------------|------------------------------|
| POST    | `/api/patients`     | Créer un nouveau patient     |
| GET     | `/api/patients`     | Lister tous les patients     |
| GET     | `/api/patients/{id}`| Récupérer un patient spécifique |
| PUT     | `/api/patients/{id}`| Mettre à jour un patient     |
| DELETE  | `/api/patients/{id}`| Supprimer un patient         |

### Fonctionnalités Spéciales
- **Associations** : Liens avec les retours et rappels.
- **Validation** : Vérification des emails et numéros de téléphone.
- **Historique** : Suivi des interactions patient.

## 📊 API Tableau de Bord (Admin/Analytique)

### Endpoints
| Méthode | Endpoint            | Description                  |
|---------|---------------------|------------------------------|
| GET     | `/api/dashboard/stats` | Récupérer les statistiques globales |
| GET     | `/api/dashboard/feedback` | Analyser les retours par catégorie |
| GET     | `/api/dashboard/reminders` | Analyser les rappels par statut |

### Fonctionnalités Spéciales
- **Filtrage** : Par date, patient ou statut.
- **Visualisation** : Données agrégées pour les rapports.
- **Accès Restreint** : Réservé aux utilisateurs avec rôle "admin".

## 🗃️ Modèles de Données

### **Utilisateur**
- **Champs** : `id`, `username`, `email`, `phone_number`, `hashed_password`, `role`, `is_active`.

### **Patient**
- **Champs** : `id`, `user_id` (optionnel), `name`, `email`, `phone_number`, `age`, `gender`, `condition`, `registration_date`.

### **Retour**
- **Champs** : `id`, `patient_id`, `patient_name`, `age`, `gender`, `phone_number`, `condition`, `treatment_satisfaction`, `communication_rating`, `facility_rating`, `overall_experience`, `recommendation_likelihood`, `feedback_date`, `comments`, `language`, `submission_method`, `sentiment`, `audio_url`, `emoji_rating`, `is_synced`, `processed`.

### **Rappel**
- **Champs** : `id`, `patient_id`, `phone_number`, `email`, `message`, `language`, `scheduled_time`, `status`, `channel`.

## 🔧 Prérequis

### Variables d'Environnement
```bash
# Base de Données
DATABASE_URL=postgresql://user:password@localhost:5432/feedback_db

# Authentification
SECRET_KEY=votre-clé-secrète
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080  # 7 jours

# Twilio
TWILIO_ACCOUNT_SID=votre_sid
TWILIO_AUTH_TOKEN=votre_token
TWILIO_PHONE_NUMBER=+237XXXXXXXX

# SMTP
SMTP_USER=votre_email@gmail.com
SMTP_PASS=votre_mot_de_passe_app
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# Google Speech-to-Text (Optionnel)
GOOGLE_APPLICATION_CREDENTIALS=chemin/vers/credentials.json
```

## 🚀 Nouveautés (Mise à jour 16 Juillet 2024)

## 📊 API Tableau de Bord (Admin/Analytics)

### Endpoints

|Méthode|Endpoint|Description|
|---------|------------------------|--------------------------------------|
|GET|	/api/dashboard/stats	|Statistiques globales (retours, rappels)|
|GET	|/api/dashboard/feedback	|Analyse des retours par catégorie|
|GET|	/api/dashboard/reminders|	Analyse des rappels par statut|

### Fonctionnalités Spéciales

- Filtrage: Par date, patient, ou statut
- Visualisation: Données agrégées pour rapports
- Accès restreint: Réservé aux utilisateurs avec rôle "admin"
- 
## 👤 API Gestion des Patients

### Endpoints

Méthode	Endpoint	Description
|---------|------------------------|--------------------------------------|
|POST	|/api/patients|Création d'un nouveau patient|
|GET	|/api/patients	|Liste tous les patients|
|GET	|/api/patients/{id}	|Détails d'un patient spécifique|
|PUT	|/api/patients/{id}	|Mise à jour d'un patient|
|DELETE	|/api/patients/{id}	|Suppression d'un patient|

### Fonctionnalités Spéciales

- Association: Lien avec retours et rappels
- Validation: Vérification des données (email, téléphone)
- Historique: Suivi des interactions patient



## Endpoints 


 ![alt text](assets/swagger1.png)


 ![alt text](assets/swagger2.png)

## 🛠️ Pile Technologique

### **Backend**
- **Python 3.10+** - Logique principale de l'application
- **FastAPI 0.100+** - Framework d'API web asynchrone
- **PostgreSQL** - Base de données principale
- **Twilio** - Gestion des notifications SMS et IVR
- **SMTP/SendGrid** - Envoi d'emails
- **Redis** - Cache pour les réponses fréquentes
- **SQLAlchemy** - ORM pour la gestion de la base de données

### **DevOps et Infrastructure**
- **Docker** - Conteneurisation
- **k3s Cluster** - Orchestration légère
- **Google Cloud** - Déploiement cloud
- **GitHub Actions** - Pipeline CI/CD

## 📊 Modèles et Données

### **Structure des données**
- **Feedbacks** : `id`, `patient_id`, `language`, `content`, `rating`, `voice_data`, `date_submitted`, `processed`.
- **Reminders** : `id`, `patient_id`, `message`, `language`, `scheduled_time`, `phone_number`, `email`, `status`.

### **Optimisation**
- **Traitement léger** - Réponses API compressées (Gzip).
- **Gestion asynchrone** - Tâches différées pour les rappels et emails.

## 🚦 Démarrage

### **Prérequis**
```bash
Python 3.10+
PostgreSQL 15+
Redis 7+
Twilio account
SendGrid API key or SMTP credentials
```

### **Installation**

1. **Cloner le dépôt**
```bash
git clone --branch Track1 --single-branch https://github.com/Delmat237/CODE2CARE_AICELLGI.git
cd CODE2CARE_AICELLGI
```

2. **Configuration Backend**
```bash
# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Remplir DATABASE_URL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, 
# SENDGRID_API_KEY ou SMTP_USER/SMTP_PASS, SECRET_KEY

# Initialiser la base de données
alembic upgrade head

# Démarrer les services
redis-server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. **Déploiement Docker**
```bash
docker-compose up --build
```

## 📈 Utilisation

### **Endpoints API**

#### **Soumission de retours**
```bash
POST /api/feedback
Content-Type: application/json

{
  "patient_id": "PAT123",
  "language": "french",
  "content": "Bon service",
  "rating": 4,
  "voice_data": "base64_encoded_audio"
}
```

#### **Planification d'un rappel**
```bash
POST /api/reminders
Content-Type: application/json

{
  "patient_id": "PAT123",
  "message": "Rappel: RDV à 10h",
  "language": "french",
  "scheduled_time": "2025-07-14T10:00:00Z",
  "phone_number": "+237XXXXXXXX",
  "email": "patient@example.com"
}
```

#### **Réponse**
```json
{
  "id": 1,
  "patient_id": "PAT123",
  "language": "french",
  "content": "Bon service",
  "rating": 4,
  "date_submitted": "2025-07-13T22:07:00Z",
  "processed": false
}
```

## 🧪 Tests

### **Tests unitaires**
```bash
pytest tests/
```

### **Tests d'intégration**
```bash
pytest tests/integration/
```

## 📊 Métriques de Performance

### **Performance du système**
- **Latence** : < 2 secondes par requête
- **Débit** : 10 000+ soumissions/jour
- **Disponibilité** : Objectif SLA 99%
- **Taille des données** : Réponses API < 1 KB

## 🔒 Fonctionnalités de Sécurité
- **Chiffrement des données** - AES-256 au repos, TLS en transit
- **Authentification API** - JWT (à implémenter)
- **Limitation de taux** - Protection contre abus
- **Conformité RGPD/HIPAA** - Protection des données patients

## 🌍 Déploiement

### **Environnement de production**
```bash
# Variables d'environnement
export DATABASE_URL="postgresql://user:pass@localhost:5432/feedback_db"
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export TWILIO_PHONE_NUMBER="+237XXXXXXX"
export SENDGRID_API_KEY="your_sendgrid_key"
export SECRET_KEY="your-secret-key"

# Déploiement avec Docker
docker-compose -f docker-compose.prod.yml up -d
```

### **Surveillance**
- **Prometheus** - Collecte des métriques
- **Grafana** - Tableaux de bord
- **Sentry** - Suivi des erreurs (à configurer)

## 🤝 Contribution

1. Forker le dépôt
2. Créer une branche de fonctionnalité (`git checkout -b feature/nouvelle-fonction`)
3. Valider les modifications (`git commit -m 'Ajout d'une nouvelle fonction'`)
4. Pousser sur la branche (`git push origin feature/nouvelle-fonction`)
5. Ouvrir une Pull Request

## 📜 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Leonel Azangue (Delmat237)**  
- GitHub : [@Delmat237](https://github.com/Delmat237)  
- LinkedIn : [leonel-azangue](https://www.linkedin.com/in/leonel-azangue)  
- Email : azangueleonel9@gmail.com  

## 🙏 Remerciements
- Équipe FastAPI pour le framework performant
- Twilio pour les services de communication
- SendGrid pour les emails
- DGH et DSWB pour le support
- Contributeurs open source

---

⭐ **Ajoutez une étoile à ce dépôt si vous le trouvez utile !**