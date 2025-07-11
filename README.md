# CODE2CARE_AICELLGI
# Hackathon IA en Santé 2025 : Solutions pour l’Hôpital Général de Douala

## Aperçu général
Ce dépôt GitHub contient les prototypes, la documentation technique, et les ressources développées lors du Hackathon IA en Santé 2025, organisé à l’Hôpital Général de Douala (DGH) en partenariat avec Data Science Without Borders (DSWB) et financé par la Wellcome Trust. Cet événement, qui s’est tenu de juillet à août 2025, vise à transformer la prestation de soins de santé au Cameroun en exploitant l’intelligence artificielle (IA) et l’apprentissage automatique pour relever des défis systémiques tels que le faible engagement des patients, la pénurie de personnel, les systèmes d’inventaire inefficaces, et l’accès limité à l’information sanitaire.

L’objectif était de réunir des équipes interdisciplinaires pour co-concevoir, prototyper, et tester des solutions IA adaptées à un déploiement réel à DGH, en tenant compte des contraintes locales comme les environnements à faible bande passante et les besoins multilingues.

## Structure du dépôt
Le dépôt est organisé en plusieurs dossiers pour faciliter l’accès aux ressources :

| **Dossier**       | **Contenu**                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `track1/`         | Fichiers pour le Système de gestion des retours et rappels des patients.    |
| `track2/`         | Fichiers pour le Chatbot pour l’éducation et le soutien des patients.        |
| `track3/`         | Fichiers pour le Système de surveillance et de prévision des stocks de sang. |
| `documentation/`  | Rapports techniques, manuels, et diapositives de présentation.              |
| `data/`           | Données synthétiques ou approuvées utilisées pour les tests.                |

Chaque module contient un fichier README détaillant les instructions pour configurer, exécuter, et tester les prototypes, incluant les dépendances logicielles et les prérequis techniques.

## Modules du Hackathon

### Track 1 : Système de gestion des retours et rappels des patients
- **Description** : Ce module propose un système intégré pour collecter les retours des patients, analyser les sentiments et thèmes à l’aide du traitement du langage naturel (NLP), et envoyer des rappels multilingues (anglais, français, Douala, Bassa, Ewondo) pour les rendez-vous et les prises de médicaments. Le système prend en charge des méthodes d’entrée visuelles (emojis, étoiles) et des interactions vocales/textuelles, optimisées pour les environnements à faible bande passante.
- **Technologies utilisées** :
  - NLP pour l’analyse des sentiments (ex. : spaCy).
  - Interfaces vocales (ex. : Google Cloud Speech-to-Text).
  - Frameworks pour applications mobiles multilingues (ex. : Flutter).
- **Contenu** :
  - Code source pour la collecte et l’analyse des retours.
  - Scripts pour les rappels automatisés.
  - Interfaces utilisateur adaptées aux contraintes locales.
- **Pertinence** : Ce système améliore l’engagement des patients dans un contexte multilingue et à faible connectivité.

### Track 2 : Chatbot pour l’éducation et le soutien des patients
- **Description** : Ce module développe un chatbot conversationnel basé sur des modèles de langage (LLM) comme Mistral ou LLaMA, conçu pour répondre aux questions des patients sur les diagnostics, les médicaments, et les instructions de soins. Le chatbot utilise un langage clair, empathique, et culturellement adapté.
- **Technologies utilisées** :
  - Modèles de langage via Hugging Face ou LangChain.
  - Traitement du langage naturel (NLP).
  - Interfaces utilisateur conversationnelles (ex. : Streamlit).
- **Contenu** :
  - Code source du chatbot.
  - Données d’entraînement pour le modèle.
  - Journaux d’interaction utilisateur pour l’évaluation.
- **Pertinence** : Ce module renforce l’autonomie des patients en facilitant l’accès à l’information sanitaire.

### Track 3 : Système de surveillance et de prévision des stocks de banque de sang
- **Description** : Ce module propose un système intelligent pour surveiller les niveaux de stock de sang, prévoir la demande future, et fournir des recommandations pour optimiser les commandes et l’allocation des ressources. Il utilise des techniques de prévision avancées et des visualisations interactives.
- **Technologies utilisées** :
  - Prévision de séries temporelles (ex. : ARIMA, XGBoost).
  - Visualisation de données (ex. : Plotly, D3.js).
  - Intégration cloud (ex. : Google Cloud, AWS).
- **Contenu** :
  - Code pour les modèles de prévision.
  - Tableaux de bord interactifs pour la visualisation des données.
  - Scripts d’intégration avec les systèmes hospitaliers.
- **Pertinence** : Ce système répond à un besoin critique de gestion efficace des ressources hospitalières.

## Instructions pour les utilisateurs
Chaque dossier de module (`track1/`, `track2/`, `track3/`) contient un fichier README avec des instructions détaillées sur :
- Les prérequis techniques (ex. : versions de Python, bibliothèques nécessaires).
- Les étapes pour configurer et exécuter le prototype.
- Les recommandations pour tester les solutions avec des données synthétiques ou approuvées.

Le dossier `documentation/` contient des rapports techniques détaillant l’architecture, les méthodes, et les outils utilisés, ainsi que des diapositives de présentation pour les parties prenantes.

## Contexte et impact
Le Hackathon IA en Santé 2025 s’inscrit dans une démarche d’innovation en santé numérique au Cameroun, suivant l’exemple de l’hôpital de Bonassama, l’un des premiers en Afrique à intégrer l’IA dans les soins de santé ([Business in Cameroon, 2017](https://www.businessincameroon.com/health/2703-7008-bonassama-hospital-among-the-first-health-structures-in-africa-to-introduce-artificial-intelligence-to-improve-healthcare)). Soutenu par la Wellcome Trust ([Wellcome](https://wellcome.org/)), ce hackathon vise à produire des solutions pratiques pour DGH, un hôpital de 630 lits avec une banque de sang et des services variés ([LSTM](https://www.lstmed.ac.uk/h%25C3%25B4pital-g%25C3%25A9n%25C3%25A9ral-de-douala)).

Ces prototypes ont le potentiel d’améliorer l’engagement des patients, de réduire la charge sur le personnel médical, et d’optimiser la gestion des ressources, avec des perspectives d’implémentation à plus grande échelle.

## Crédits et remerciements
Ce dépôt reflète le travail collaboratif d’équipes interdisciplinaires composées de cliniciens, data scientists, développeurs, et designers. Nous remercions la Wellcome Trust pour son financement, DGH et DSWB pour leur soutien organisationnel, et tous les participants pour leur engagement envers l’innovation en santé numérique.

Pour plus d’informations ou pour contribuer au développement des prototypes, consultez les sites officiels de DGH ([Hôpital Général de Douala](https://demo.hgd.cm/)) et de la Wellcome Trust ([Wellcome](https://wellcome.org/)).
