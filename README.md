# 🏥 Assistant Médical Africain

Un chatbot médical conversationnel basé sur l'IA, spécialement adapté au contexte africain. Ce projet utilise des modèles de langage open source pour fournir des conseils médicaux empathiques, culturellement appropriés et sécurisés.

##  Iamge

 interface de conversation

![alt text](<Capture d’écran du 2025-07-22 12-07-21.png>)

interface pour les ressources tiers

![alt text](<Capture d’écran du 2025-07-22 12-07-39.png>)

## 🌟 Caractéristiques

### 🤖 Intelligence Artificielle
- **Modèle LLM**: Mistral-7B-Instruct ou LLaMA via Hugging Face
- **Traitement multilingue**: Français, Anglais, Wolof, Hausa, Swahili
- **Adaptation culturelle**: Contexte africain intégré
- **Évaluation qualité**: Scoring automatique des réponses

### 🏗️ Architecture
- **Backend**: FastAPI avec API REST sécurisée
- **Frontend**: Double option React (moderne) + Streamlit (simple)
- **Base de données**: SQLite avec chiffrement optionnel
- **Authentification**: JWT pour la sécurité

### 🛡️ Sécurité et Confidentialité
- Chiffrement des conversations
- Authentification des utilisateurs
- Gestion des sessions sécurisée
- Conformité RGPD

### 🌍 Adaptation Culturelle
- Prise en compte des langues locales
- Adaptation aux ressources médicales disponibles
- Respect des traditions et pratiques locales
- Interface multilingue complète

## 📋 Prérequis Système

### Configuration Minimale
- **Python**: 3.8 ou supérieur
- **RAM**: 8 GB minimum (16 GB recommandé)
- **Stockage**: 10 GB d'espace libre
- **GPU**: Optionnel mais recommandé (CUDA compatible)

### Dépendances Principales
- `transformers` pour les modèles LLM
- `fastapi` pour l'API backend
- `streamlit` pour l'interface simple
- `react` pour l'interface avancée
- `sqlalchemy` pour la base de données

## 🚀 Installation

### 1. Cloner le Projet
```bash
git clone <repository-url>
cd medical-chatbot-african
```

### 2. Installation Automatique
```bash
python scripts/setup_environment.py
```

### 3. Installation Manuelle
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 4. Configuration
```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer le fichier .env avec vos paramètres
# Notamment votre token Hugging Face
```

## ⚙️ Configuration

### Variables d'Environnement Importantes

```env
# Token Hugging Face (obligatoire)
HF_API_TOKEN=your_huggingface_token_here

# Modèle à utiliser
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1

# Configuration de sécurité
SECRET_KEY=your_secret_key_here
ENCRYPT_CONVERSATIONS=True

# Langues supportées
SUPPORTED_LANGUAGES=fr,en,wolof,hausa,swahili
```

### Obtenir un Token Hugging Face
1. Créer un compte sur [Hugging Face](https://huggingface.co/)
2. Aller dans Settings > Access Tokens
3. Créer un nouveau token avec les permissions de lecture
4. Copier le token dans votre fichier `.env`

## 🏃‍♂️ Démarrage

### Option 1: Interface Streamlit (Recommandée pour débuter)
```bash
# Démarrer le backend
python -m backend.main

# Dans un nouveau terminal, démarrer Streamlit
streamlit run frontend_streamlit/app.py
```

### Option 2: Interface React (Interface moderne)
```bash
# Démarrer le backend
python -m backend.main

# Dans un nouveau terminal, démarrer React
npm install
npm run dev
```

### Accès aux Interfaces
- **Streamlit**: http://localhost:8501
- **React**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

## 🧪 Tests

### Exécution des Tests
```bash
# Tests complets
python scripts/run_tests.py

# Tests unitaires seulement
pytest tests/ -v

# Tests de qualité du code
flake8 backend/ --max-line-length=120
```

### Tests d'Intégration
Le système inclut des tests d'intégration avec des conversations prédéfinies pour évaluer:
- La qualité des réponses
- L'empathie du chatbot
- La sécurité médicale
- L'adaptation culturelle

## 📊 Évaluation et Monitoring

### Métriques d'Évaluation
- **Score d'empathie**: Évalue la bienveillance des réponses
- **Score de sécurité**: Vérifie les recommandations médicales
- **Adaptation culturelle**: Mesure la pertinence contextuelle
- **Confiance**: Niveau de certitude des réponses

### Monitoring
- Logs détaillés des conversations
- Métriques de performance
- Alertes de sécurité
- Statistiques d'utilisation

## 🗂️ Structure du Projet

```
medical-chatbot-african/
├── backend/                    # API FastAPI
│   ├── main.py                # Point d'entrée API
│   ├── chatbot.py             # Logique du chatbot
│   ├── models.py              # Modèles de données
│   ├── database.py            # Configuration DB
│   ├── auth.py                # Authentification
│   ├── privacy.py             # Chiffrement
│   ├── evaluation.py          # Évaluation qualité
│   ├── language_adapter.py    # Adaptation linguistique
│   └── config.py              # Configuration
├── frontend_streamlit/         # Interface Streamlit
│   └── app.py                 # Application Streamlit
├── src/                       # Interface React
│   ├── App.tsx                # Composant principal
│   └── ...                    # Autres composants
├── data/                      # Données et connaissances
│   ├── medical_knowledge.json # Base de connaissances
│   └── test_conversations.json # Conversations test
├── tests/                     # Tests unitaires
│   └── test_chatbot.py        # Tests du chatbot
├── scripts/                   # Scripts utilitaires
│   ├── setup_environment.py   # Installation
│   └── run_tests.py           # Tests
├── requirements.txt           # Dépendances Python
├── package.json              # Dépendances React
└── README.md                 # Documentation
```

## 🎯 Utilisation

### Démarrage d'une Conversation
1. Ouvrir l'interface (Streamlit ou React)
2. Sélectionner la langue préférée
3. Optionnel: Remplir le contexte utilisateur (âge, localisation)
4. Commencer à poser des questions médicales

### Exemples de Questions
- "J'ai de la fièvre depuis 2 jours, que faire?"
- "Mon enfant a la diarrhée, dois-je m'inquiéter?"
- "Quelle est la posologie du paracétamol?"
- "Comment prévenir le paludisme?"

### Fonctionnalités Avancées
- **Historique**: Toutes les conversations sont sauvegardées
- **Multilingue**: Changement de langue en temps réel
- **Suggestions**: Questions de suivi proposées
- **Évaluation**: Chaque réponse est évaluée pour la qualité

## 🔒 Sécurité et Conformité

### Mesures de Sécurité
- **Chiffrement**: Conversations chiffrées en base
- **Authentification**: JWT pour l'accès API
- **Validation**: Validation stricte des entrées
- **Logs**: Audit trail complet

### Conformité Médicale
- **Disclaimers**: Avertissements systématiques
- **Références**: Orientation vers professionnels
- **Éthique**: Évitement des diagnostics définitifs
- **Culturel**: Respect des pratiques locales

## 🤝 Contribution

### Comment Contribuer
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards de Code
- **Python**: PEP 8 avec flake8
- **TypeScript**: ESLint configuration
- **Tests**: Coverage minimum 80%
- **Documentation**: Docstrings obligatoires

## 📚 Documentation Technique

### API Endpoints
- `POST /chat`: Envoyer un message
- `GET /history/{session_id}`: Récupérer l'historique
- `DELETE /history/{session_id}`: Supprimer l'historique
- `GET /health`: Vérifier l'état du service
- `GET /languages`: Langues supportées

### Modèles de Données
- **ChatRequest**: Requête utilisateur
- **ChatResponse**: Réponse du chatbot
- **ConversationHistory**: Historique des conversations
- **User**: Informations utilisateur

## 🌟 Feuille de Route

### Version 1.1 (Prochaine)
- [ ] Support de nouveaux modèles LLM
- [ ] Interface mobile dédiée
- [ ] Intégration avec bases de données médicales
- [ ] Mode hors ligne

### Version 1.2 (Future)
- [ ] Reconnaissance vocale
- [ ] Synthèse vocale multilingue
- [ ] Intégration avec systèmes hospitaliers
- [ ] Analyse prédictive

## 📞 Support

### Documentation
- **Wiki**: Documentation complète en ligne
- **FAQ**: Questions fréquemment posées
- **Tutorials**: Guides pas à pas

### Contact
- **Issues**: Utiliser GitHub Issues pour les bugs
- **Discussions**: GitHub Discussions pour les questions
- **Email**: support@medical-chatbot-african.org

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Hugging Face**: Pour les modèles LLM
- **Mistral AI**: Pour le modèle Mistral-7B
- **Meta**: Pour le modèle LLaMA
- **Communauté Open Source**: Pour les outils et bibliothèques

---

**⚠️ Avertissement Important**: Ce chatbot est un outil d'information et ne remplace pas une consultation médicale professionnelle. En cas d'urgence médicale, contactez immédiatement les services d'urgence locaux.

**🌍 Développé avec ❤️ pour l'Afrique**