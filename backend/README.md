# 🛠️ Patient Education and Support Backend

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-orange.svg)

> **Backend API pour l'éducation et le soutien des patients à Douala General Hospital**

## 📌 Table of Contents

- [Fonctionnalités](#-fonctionnalités)
    - [Fonctionnalités principales](#fonctionnalités-principales)
    - [Intégration et API](#intégration-et-api)
- [Architecture du système](#-architecture)
- [Arborescence expliquée](#-arborescence-expliquée)
- [Vue d'Ensemble des Fichiers et Dossiers](#-vue-densemble-des-fichiers-et-dossiers)
- [Roadmap](#-prochaines-étapes-dici-le-25-juillet-2025)
- [Pile Technologique](#-pile-technologique)
- [Modèle de données](#-modèles-de-données)
- [Setup Guide](#-démarrage)
- [Utilisation](#-utilisation)
- [How to Contribute](#-contribution)

Une API backend robuste et scalable développée avec FastAPI pour gérer les requêtes des patients, interagir avec un LLM séparé via LangChain, et fournir des réponses multilingues (anglais, français, Douala, Bassa, Ewondo), optimisée pour les zones à faible bande passante.

## 🚀 Fonctionnalités

### **Fonctionnalités principales**

- **Réception des Requêtes** : Collecte des questions texte/voix des patients dans 5 langues.
- **Gestion des Données** : Stockage des requêtes et réponses dans une base de données.
- **Intégration LLM** : Utilisation de LangChain pour interagir avec un modèle de langage séparé.
- **Réponses Automatisées** : Fournit des réponses éducatives personnalisées via le frontend.

### **Intégration et API**

- **API RESTful** : Endpoints pour recevoir et renvoyer les requêtes/réponses.
- **Support Multilingue** : Intégration avec Google Translate pour les traductions.
- **Traitement Léger** : Optimisé pour faible bande passante (< 256 kbps).
- **Support JSON** : Format standard pour les échanges API.

## 🏗️ Architecture
```
┌────────────────────┐    ┌────────────────────┐
│   API Backend      │    │   Base de données  │
│   (FastAPI)        │◄──►│   (PostgreSQL)     │
└────────────────────┘    └────────────────────┘
        │                        │
        │                        ▼
        ├────────┐               ┌────────────────────┐
        │        └──────►│   Modèle LLM (Séparé)    │
        │                │   (via LangChain)        │
        │                └────────────────────┘
        ▼
┌────────────────────┐
│   Frontend (Next.js)│
└────────────────────┘
```

## 🌳 Arborescence expliquée

```
backend/
│
├── backend.py              # Point d'entrée de l'application FastAPI
├── config/                 # Configuration et variables d'environnement
│   └── settings.py         # Paramètres globaux avec Pydantic BaseSettings
├── database/               # Gestion de la base de données
│   ├── __init__.py        # Initialisation du module
│   ├── database.py        # Connexion SQLAlchemy et gestion des sessions
│   └── migrations/        # Scripts de migration Alembic
│       ├── env.py         # Configuration de l'environnement de migration
│       ├── script.py.mako # Modèle de script de migration
│       └── versions/      # Versions de migration générées
├── models/                 # Modèles SQLAlchemy pour la persistance
│   ├── __init__.py        # Initialisation du module
│   └── query_log.py       # Modèle QueryLog
├── schemas/                # Schémas Pydantic pour la validation
│   ├── __init__.py        # Initialisation du module
│   └── query.py           # Schéma QueryRequest et QueryResponse
├── utils/                  # Utilitaires et intégrations externes
│   ├── __init__.py        # Initialisation du module
│   └── langchain_client.py # Intégration avec LangChain
├── tests/                  # Tests unitaires et d'intégration
│   ├── __init__.py        # Initialisation du module
│   ├── test_api.py        # Tests des endpoints
│   └── integration/       # Tests d'intégration (à développer)
├── alembic.ini             # Configuration principale d'Alembic
├── requirements.txt        # Dépendances Python
├── .env.example            # Exemple de fichier de variables d'environnement
├── docker-compose.yml      # Configuration Docker pour le développement
└── README.md               # Documentation du projet
```

## 📋 Vue d'Ensemble des Fichiers et Dossiers

### **`backend.py`**

- **Rôle** : Point d'entrée de l'application FastAPI avec configuration CORS, inclusion des routers, et lancement avec Uvicorn (hôte : `0.0.0.0`, port : `8000`).

### **`config/settings.py`**

- **Rôle** : Gère les configurations avec Pydantic (`DATABASE_URL`, `MODEL_API_URL`, `SECRET_KEY`, etc.) chargées depuis `.env`.

### **`database/`**

- **database.py** : Gère la connexion à PostgreSQL avec SQLAlchemy et fournit la dépendance `get_db`.
- **migrations/** : Utilise Alembic pour gérer les schémas de la base de données (ex. `query_logs`).

### **`models/`**

- **query_log.py** : Modèle SQLAlchemy pour la table `query_logs` (stockage des requêtes et réponses).

### **`schemas/`**

- **query.py** : Schémas Pydantic pour valider les requêtes (`QueryRequest`) et réponses (`QueryResponse`).

### **`utils/`**

- **langchain_client.py** : Intègre LangChain pour interagir avec le LLM séparé.

### **`tests/`**

- **test_api.py** : Tests unitaires pour les endpoints.
- **integration/** : Dossier pour les tests d'intégration (à développer).

### **Fichiers de Configuration**

- **alembic.ini** : Configuration principale d'Alembic.
- **requirements.txt** : Liste des dépendances (ex. `fastapi`, `sqlalchemy`, `langchain`).
- **.env.example** : Modèle de fichier de variables d'environnement avec commentaires.
- **docker-compose.yml** : Définit les services (app, PostgreSQL) pour le développement.

## ⚙️ Considérations de Conception

- **Modularité** : Composants isolés pour une maintenance facile.
- **Scalabilité** : Conçu pour gérer jusqu'à 1 000 utilisateurs simultanés.
- **Optimisation Faible Bande Passante** : Réponses compressées (Gzip), gestion asynchrone.
- **Sécurité** : Authentification JWT, chiffrement TLS (à configurer).

## ⏰ Prochaines Étapes (d'ici le 25 juillet 2025)

- **22 Jul 2025** : Configuration finale et tests initiaux des endpoints.
- **23 Jul 2025** : Intégration complète avec LangChain et le modèle LLM.
- **24 Jul 2025** : Optimisation pour faible bande passante et tests d'intégration avec le frontend.
- **25 Jul 2025** : Livraison du prototype et documentation finale.

## 🛠️ Pile Technologique

### **Backend**

- **Python 3.9+** - Logique principale de l'application
- **FastAPI 0.100+** - Framework d'API web asynchrone
- **PostgreSQL** - Base de données principale
- **LangChain** - Intégration avec le LLM séparé
- **Google Translate** - Support multilingue (optionnel)

### **DevOps et Infrastructure**

- **Docker** - Conteneurisation
- **Google Cloud** - Déploiement cloud (optionnel)
- **GitHub Actions** - Pipeline CI/CD (optionnel)

## 📊 Modèles de Données

### **QueryLog**

- **Champs** : `id`, `query`, `language`, `timestamp`, `response`

## 🔧 Prérequis

### Variables d'Environnement

```bash
# Base de Données
DATABASE_URL=postgresql://user:password@localhost:5432/dgh_db

# Authentification
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# Modèle LLM
MODEL_API_URL=http://model-api:8000/query
```

## 🚦 Démarrage

### **Prérequis**

```bash
Python 3.9+
PostgreSQL 15+
```

### **Installation**

1. **Cloner le dépôt**
   ```bash
   git clone --branch Track2/backend/AZANGUE --single-branch https://github.com/Delmat237/CODE2CARE_AICELLGI.git

   cd backend
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
   # Remplir DATABASE_URL, MODEL_API_URL, SECRET_KEY

   # Initialiser la base de données
   alembic upgrade head

   # Démarrer le serveur
   uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Déploiement Docker**

   ```bash
   docker-compose up --build
   ```

## 📈 Utilisation

### **Endpoints API**

#### **Soumission de Requêtes**

```bash
POST /receive_query
Content-Type: application/json
Authorization: Bearer <token>

{
  "query": "Que signifie mon diagnostic?",
  "language": "fr"
}
```

#### **Récupération de Réponses**

```bash
GET /send_response/{query_id}
Authorization: Bearer <token>
```

#### **Réponse**

```json
{
  "response": "Votre diagnostic signifie...",
  "status": "success"
}
```

## 🧪 Tests

### **Tests unitaires**

```bash
pytest tests/
```

## 📊 Métriques de Performance

- **Latence** : < 2 secondes par requête texte, < 5 secondes pour voix
- **Débit** : 1 000+ requêtes/jour
- **Disponibilité** : Objectif SLA 99%

## 🔒 Fonctionnalités de Sécurité

- **Chiffrement des données** : TLS en transit (à configurer)
- **Authentification API** : JWT
- **Limitation de taux** : Protection contre abus (à implémenter)

## 🌍 Déploiement

### **Environnement de production**
```bash
# Variables d'environnement
export DATABASE_URL="postgresql://user:pass@localhost:5432/dgh_db"
export MODEL_API_URL="http://model-api:8000/query"
export SECRET_KEY="your-secret-key"

# Déploiement avec Docker
docker-compose up -d
```

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
- Email : [azangueleonel9@gmail.com](mailto:azangueleonel9@gmail.com)

## 🙏 Remerciements

- Équipe AICELLGI
- Équipe FastAPI pour le framework performant
- LangChain pour l'intégration LLM
- DGH et DSWB pour le support
- Contributeurs open source

---

⭐ **Ajoutez une étoile à ce dépôt si vous le trouvez utile !**