# 🛠️ Patient Feedback and Reminder Backend

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-orange.svg)

> **Backend API pour la gestion des retours patients et rappels à Douala General Hospital**

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
│   └── settings.py          # Paramètres globaux (BaseSettings avec Pydantic)
├── database/                # Gestion de la base de données
│   ├── __init__.py          # Initialisation du module (vide ou import)
│   ├── database.py          # Connexion SQLAlchemy et session management
│   └── migrations/          # Migrations Alembic pour la base de données
│       ├── env.py           # Environnement de migration
│       ├── script.py.mako   # Modèle de script de migration
│       └── versions/        # Versions des migrations (générées par Alembic)
├── models/                  # Schémas Pydantic pour les données
│   ├── __init__.py          # Initialisation du module
│   ├── feedback.py          # Modèles pour les retours patients
│   └── reminder.py          # Modèles pour les rappels
├── schemas/                 # Modèles SQLAlchemy pour la persistance
│   ├── __init__.py          # Initialisation du module
│   ├── feedback.py          # Table Feedback dans PostgreSQL
│   └── reminder.py          # Table Reminder dans PostgreSQL
├── routers/                 # Définitions des endpoints API
│   ├── __init__.py          # Initialisation du module
│   ├── feedback.py          # Endpoints pour la soumission de retours
│   └── reminders.py         # Endpoints pour la planification de rappels
├── utils/                   # Utilitaires et services externes
│   ├── __init__.py          # Initialisation du module
│   ├── twilio_client.py     # Intégration Twilio pour SMS/IVR
│   └── email_client.py      # Intégration SMTP/SendGrid pour emails
├── tests/                   # Tests unitaires et d'intégration
│   ├── __init__.py          # Initialisation du module
│   ├── test_feedback.py     # Tests pour les endpoints feedback
│   ├── test_reminders.py    # Tests pour les endpoints reminders
│   └── integration/         # Tests d'intégration (à développer)
├── alembic.ini              # Configuration principale d'Alembic
├── requirements.txt         # Liste des dépendances Python
├── .env.example             # Exemple de fichier de variables d'environnement
├── docker-compose.yml       # Configuration Docker pour le développement
├── docker-compose.prod.yml  # Configuration Docker pour la production
└── README.md # document d'explication

```

## 📋 Explication des dossiers et fichiers

### **`main.py`**

- **Rôle** : Point d'entrée de l'application FastAPI. Configure CORS, inclut les routers, et lance le serveur avec Uvicorn.
- **Détails** : Définit l'host (`0.0.0.0`) et le port (`8000`) pour une accessibilité externe.

### **`config/`**

- **settings.py** : Contient les configurations via Pydantic (`DATABASE_URL`, `TWILIO_*`, `SENDGRID_API_KEY`, etc.) chargées depuis `.env`.

### **`database/`**

- **database.py** : Gère la connexion à PostgreSQL avec SQLAlchemy et fournit une dépendance `get_db` pour les sessions.
- **migrations/** : Utilise Alembic pour gérer les schémas de la base de données (création de tables `feedbacks` et `reminders`).

### **`models/`**

- **feedback.py** : Définit les schémas Pydantic (`FeedbackCreate`, `FeedbackResponse`) pour valider les données d'entrée/sortie des retours.
- **reminder.py** : Définit les schémas Pydantic (`ReminderCreate`, `ReminderResponse`) pour les rappels.

### **`schemas/`**

- **feedback.py** : Modèle SQLAlchemy pour la table `feedbacks` avec colonnes comme `patient_id`, `language`, etc.
- **reminder.py** : Modèle SQLAlchemy pour la table `reminders` avec colonnes comme `scheduled_time`, `email`, etc.

### **`routers/`**

- **feedback.py** : Contient l'endpoint `POST /api/feedback` pour soumettre des retours.
- **reminders.py** : Contient l'endpoint `POST /api/reminders` pour planifier des rappels (SMS/IVR/email).

### **`utils/`**

- **twilio_client.py** : Intègre Twilio pour envoyer des SMS et initier des appels IVR.
- **email_client.py** : Intègre SMTP/SendGrid pour envoyer des notifications par email.

### **`tests/`**

- **test_feedback.py** : Tests unitaires pour l'endpoint de soumission de retours.
- **test_reminders.py** : Tests unitaires pour l'endpoint de rappels.
- **integration/** : Dossier pour les tests d'intégration (à développer).

### **Fichiers de configuration**

- **alembic.ini** : Configuration principale pour les migrations de la base de données.
- **requirements.txt** : Liste des dépendances (ex. `fastapi`, `sqlalchemy`, `twilio`, `sendgrid`).
- **.env.example** : Modèle pour les variables d'environnement avec commentaires.
- **docker-compose.yml** : Définit les services (app, PostgreSQL, Redis) pour le développement.
- **docker-compose.prod.yml** : Configuration pour un environnement de production avec k3s.

## ⚙️ Considérations de conception

- **Modularité** : Chaque composant (routes, modèles, utilitaires) est isolé pour faciliter les mises à jour.
- **Scalabilité** : Utilisation de k3s pour une orchestration légère et Redis pour le caching.
- **Optimisation faible bande passante** : Réponses API compressées (Gzip), gestion asynchrone des tâches.
- **Sécurité** : Préparation pour JWT et chiffrement TLS (à configurer au niveau du serveur).

## ⏰ Prochaines étapes (jusqu'au 18 juillet 2025)

- Implémenter les tests d'intégration dans `tests/integration/`.
- Ajouter la transcription vocale dans `utils/` (Google Speech-to-Text).
- Configurer l'authentification JWT dans `main.py` et `routers/`.
- Documenter les endpoints dans un fichier `openapi.json` généré par FastAPI.

## 🚀 Nouveautés (Mise à jour 14 Juillet 2024)

### **Fonctionnalités Ajoutées**
- **Système d'authentification complet** avec JWT (access + refresh tokens)
- **CRUD complet** pour les retours patients (feedback)
- **CRUD complet** pour les rappels (reminders)
- **Initialisation du Traitement vocal** intégré via Google Speech-to-Text

## 🔐 Authentification

### **Endpoints**
- `POST /api/auth/login` - Authentification avec username/password
- `POST /api/auth/register` - Creation d'un compte
- `POST /api/auth/refresh` - Rafraîchissement du token
- `POST /api/auth/logout` - Invalidation du refresh token
- `GET /api/auth/me` - Récupération des infos utilisateur

### **Sécurité**
- Tokens JWT signés avec clé secrète
- Refresh tokens stockés en base de données
- Expiration configurable (30 min pour access token, 7 jours pour refresh token)

## 📝 API Feedback (CRUD Complet)

### **Endpoints**
| Méthode | Endpoint                | Description                          |
|---------|-------------------------|--------------------------------------|
| POST    | `/api/feedback`         | Soumission d'un nouveau retour       |
| GET     | `/api/feedback`         | Liste tous les retours               |
| GET     | `/api/feedback/{id}`    | Détails d'un retour spécifique       |
| PUT     | `/api/feedback/{id}`    | Mise à jour d'un retour              |
| DELETE  | `/api/feedback/{id}`    | Suppression d'un retour              |

### **Fonctionnalités Spéciales**

- **Traitement vocal** : Transcription automatique des enregistrements
- **Traduction** : Conversion des retours en français si soumis en langue locale
- **Validation** : Modèles Pydantic stricts pour les entrées/sorties

## ⏰ API Rappels (CRUD Complet)

### **Endpoints**
| Méthode | Endpoint                | Description                          |
|---------|-------------------------|--------------------------------------|
| POST    | `/api/reminders`        | Création d'un nouveau rappel         |
| GET     | `/api/reminders`        | Liste tous les rappels               |
| GET     | `/api/reminders/{id}`   | Détails d'un rappel spécifique       |
| PUT     | `/api/reminders/{id}`   | Mise à jour d'un rappel              |
| DELETE  | `/api/reminders/{id}`   | Suppression d'un rappel              |

### **Fonctionnalités Spéciales**
- **Planification flexible** : Dates/heures configurables
- **Multi-canaux** : Rappels par SMS, appel IVR ou email
- **Statut de livraison** : Suivi de l'état des rappels

## 🗃️ Nouveaux Modèles de Données

### **Feedback**
```python
class FeedbackCreate(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True, nullable=True)
    patient_name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    condition = Column(String, nullable=False)
    treatment_satisfaction = Column(Integer, nullable=False)
    communication_rating = Column(Integer, nullable=False)
    facility_rating = Column(Integer, nullable=False)
    overall_experience = Column(Integer, nullable=False)
    recommendation_likelihood = Column(Integer, nullable=False)
    feedback_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    comments = Column(String, nullable=False)
    language = Column(String, nullable=False)
    submission_method = Column(String, nullable=False)  # Store as string, validated by enum
    sentiment = Column(String, nullable=True)  # Store as string, validated by enum
    audio_url = Column(String, nullable=True)
    emoji_rating = Column(String, nullable=True)
    is_synced = Column(Boolean, default=False, nullable=False)

class FeedbackResponse(BaseModel):
    id: int
    patient_id: str
    language: str
    content: Optional[str]
    rating: Optional[int]
    processed: bool
    comments: Optional[str]  # Texte transcrit/traduit
```

### **Reminder**
```python
class ReminderCreate(BaseModel):
    patient_id: str
    message: str
    language: str
    scheduled_time: datetime
    phone_number: str
    email: Optional[str]

class ReminderResponse(BaseModel):
    id: int
    status: str  # pending/sent/failed
    
  ```
## 🔧 Configuration Requise
Nouvelles Variables d'Environnement
```bash
# Authentification
SECRET_KEY="votre_cle_secrete"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080  # 7 jours

# Google Speech-to-Text
GOOGLE_APPLICATION_CREDENTIALS="chemin/vers/credentials.json"
```
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