# DGH Patient Feedback System

## 📋 Vue d'ensemble

Le **DGH Patient Feedback System** est une application web moderne développée pour Douala General Hospital (DGH) permettant la collecte, l'analyse et la gestion des retours patients. Le système supporte 5 langues locales et est optimisé pour les environnements à faible bande passante typiques du Cameroun.

## 🌟 Fonctionnalités Principales

### 🌍 Multilinguisme
- **5 langues supportées** : Anglais, Français, Douala, Bassa, Ewondo
- **Détection automatique** de la langue du navigateur
- **Traductions natives** validées par des locuteurs natifs
- **Persistance** du choix de langue

### 📱 Interface de Collecte Multi-Canaux
- **Application web responsive** optimisée pour tous les appareils
- **Enregistrement vocal** avec WebRTC (limité à 10 secondes)
- **Système d'étoiles** (1-5) pour les évaluations détaillées
- **Évaluation par emojis** (😢😞😐😊😍) pour une interaction intuitive
- **Slider de recommandation** (0-10) pour le calcul du Net Promoter Score
- **Commentaires textuels** multilingues

### 🔄 Mode Hors Ligne Avancé
- **Service Worker** pour le fonctionnement hors ligne
- **Stockage local IndexedDB** pour les données non synchronisées
- **Synchronisation automatique** au retour de connexion
- **Queue de retry** pour les soumissions échouées
- **Indicateur de statut réseau** en temps réel

### 📊 Dashboard Analytics
- **Métriques en temps réel** (satisfaction moyenne, NPS, communication)
- **Analyse des sentiments** automatique (positif/neutre/négatif)
- **Répartition par condition médicale**
- **Filtrage avancé** par nom, condition, genre, langue
- **Visualisations interactives** avec graphiques et barres de progression
- **Insights automatiques** et recommandations d'amélioration

### ⚡ Optimisation Faible Bande Passante
- **Taille totale < 500KB** pour l'application
- **Compression des données** et optimisation des requêtes
- **Lazy loading** des ressources
- **Compression audio** optimisée (WebM/Opus)
- **Fallbacks intelligents** en cas de connexion instable

## 🛠️ Technologies Utilisées

### Frontend
- **Next.js 13+** avec App Router
- **React 18** avec hooks modernes
- **TypeScript** pour la sécurité des types
- **Tailwind CSS** pour le design responsive
- **shadcn/ui** pour les composants UI
- **Lucide React** pour les icônes

### Stockage & Synchronisation
- **IndexedDB** pour le stockage local
- **Service Workers** pour le mode hors ligne
- **Context API** pour la gestion d'état globale

### Optimisations
- **PWA** (Progressive Web App) compliant
- **WebRTC** pour l'enregistrement audio
- **Compression Gzip** des réponses
- **CDN ready** pour les assets statiques

## 🚀 Installation et Démarrage

### Prérequis
- Node.js 18+ 
- npm ou yarn

### Installation
```bash
# Cloner le repository
git clone [repository-url]
cd dgh-patient-feedback-system

# Installer les dépendances
npm install

# Démarrer en mode développement
npm run dev
```

### Scripts Disponibles
```bash
npm run dev      # Démarrage en mode développement
npm run build    # Build de production
npm run start    # Démarrage du serveur de production
npm run lint     # Vérification du code
```

## 📁 Structure du Projet

```
dgh-patient-feedback-system/
├── app/                          # Pages Next.js (App Router)
│   ├── feedback/                 # Page de soumission de feedback
│   ├── layout.tsx               # Layout principal
│   ├── page.tsx                 # Dashboard principal
│   └── providers.tsx            # Providers React
├── components/                   # Composants réutilisables
│   ├── ui/                      # Composants UI de base (shadcn/ui)
│   ├── emoji-rating.tsx         # Composant d'évaluation par emojis
│   ├── feedback-form.tsx        # Formulaire principal de feedback
│   ├── language-selector.tsx    # Sélecteur de langue
│   ├── network-status.tsx       # Indicateur de statut réseau
│   ├── star-rating.tsx          # Composant d'évaluation par étoiles
│   └── voice-recorder.tsx       # Enregistreur vocal
├── lib/                         # Utilitaires et logique métier
│   ├── language-context.tsx     # Context pour la gestion des langues
│   ├── network-utils.ts         # Utilitaires réseau et retry logic
│   ├── offline-storage.ts       # Gestion du stockage hors ligne
│   ├── translations.ts          # Traductions multilingues
│   ├── types.ts                 # Types TypeScript
│   └── utils.ts                 # Utilitaires généraux
├── public/                      # Assets statiques
│   ├── manifest.json            # Manifest PWA
│   └── sw.js                    # Service Worker
└── styles/                      # Styles globaux
    └── globals.css              # Styles Tailwind CSS
```

## 🌐 Support Multilingue

### Langues Supportées
- **Anglais (en)** - Langue par défaut
- **Français (fr)** - Langue officielle du Cameroun
- **Douala (dua)** - Langue locale de Douala
- **Bassa (bas)** - Langue locale du Cameroun
- **Ewondo (ewo)** - Langue locale du Cameroun

### Ajout d'une Nouvelle Langue
1. Ajouter la langue dans `lib/translations.ts` :
```typescript
export const languages = [
  // ... langues existantes
  { code: 'new_lang', name: 'New Language', nativeName: 'Langue Native' }
];
```

2. Ajouter les traductions pour chaque clé :
```typescript
export const translations = {
  'key.example': {
    en: 'English text',
    fr: 'Texte français',
    // ... autres langues
    new_lang: 'Texte dans la nouvelle langue'
  }
};
```

## 📱 Mode Hors Ligne

### Fonctionnalités Hors Ligne
- **Collecte de feedback** même sans connexion internet
- **Stockage local sécurisé** avec IndexedDB
- **Synchronisation automatique** au retour de connexion
- **Indicateurs visuels** du statut de connexion
- **Queue de retry** pour les soumissions échouées

### Gestion des Données
- Les feedbacks sont sauvegardés localement avec un flag `is_synced: false`
- Lors du retour de connexion, les données non synchronisées sont automatiquement envoyées
- Les enregistrements audio sont également stockés localement et synchronisés

## 🔧 Configuration

### Variables d'Environnement
Créer un fichier `.env.local` :
```env
# API Configuration
NEXT_PUBLIC_API_URL=https://your-api-url.com
NEXT_PUBLIC_APP_ENV=development

# Analytics (optionnel)
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

### Personnalisation
- **Couleurs** : Modifier les variables CSS dans `app/globals.css`
- **Traductions** : Ajouter/modifier dans `lib/translations.ts`
- **Conditions médicales** : Modifier la liste dans `components/feedback-form.tsx`

## 📊 Analytics et Métriques

### Métriques Collectées
- **Satisfaction globale** (moyenne des évaluations)
- **Net Promoter Score (NPS)** calculé automatiquement
- **Répartition par condition médicale**
- **Analyse des sentiments** des commentaires
- **Méthodes de soumission** (web, SMS, USSD, IVR, voice)
- **Distribution par langue**

### Insights Automatiques
- Identification des **tendances positives**
- Détection des **zones d'amélioration**
- **Alertes** pour les feedbacks négatifs nécessitant attention
- **Recommandations** basées sur les données

## 🔒 Sécurité et Conformité

### Mesures de Sécurité
- **Chiffrement TLS** pour toutes les transmissions
- **Validation** côté client et serveur
- **Sanitisation** des données utilisateur
- **Gestion sécurisée** des enregistrements audio

### Conformité
- **HIPAA** ready pour les données de santé
- **GDPR** compliant pour la protection des données
- **Anonymisation** optionnelle des données sensibles

## 🚀 Déploiement

### Déploiement Vercel (Recommandé)
```bash
# Installer Vercel CLI
npm i -g vercel

# Déployer
vercel --prod
```

### Déploiement Manuel
```bash
# Build de production
npm run build

# Démarrer le serveur
npm start
```

### Optimisations de Production
- **Compression Gzip** activée
- **Mise en cache** des assets statiques
- **Optimisation des images** automatique
- **Code splitting** pour un chargement rapide

## 🧪 Tests

### Tests Unitaires
```bash
# Lancer les tests (à implémenter)
npm run test

# Tests avec couverture
npm run test:coverage
```

### Tests d'Accessibilité
- **Lighthouse** pour les performances
- **axe-core** pour l'accessibilité
- **Tests manuels** sur différents appareils

## 📈 Performance

### Métriques Cibles
- **First Contentful Paint** < 1.5s
- **Largest Contentful Paint** < 2.5s
- **Time to Interactive** < 3s
- **Cumulative Layout Shift** < 0.1

### Optimisations Implémentées
- **Lazy loading** des composants
- **Code splitting** automatique
- **Compression des images** WebP
- **Service Worker** pour la mise en cache

## 🤝 Contribution

### Guidelines de Contribution
1. **Fork** le repository
2. Créer une **branche feature** (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commit** les changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une **Pull Request**

### Standards de Code
- **TypeScript** strict mode
- **ESLint** et **Prettier** pour le formatage
- **Conventional Commits** pour les messages de commit
- **Tests unitaires** pour les nouvelles fonctionnalités

## 📞 Support

### Contact
- **Email** : support@dgh-feedback.com
- **Documentation** : [docs.dgh-feedback.com](https://docs.dgh-feedback.com)
- **Issues** : [GitHub Issues](https://github.com/your-repo/issues)

### FAQ
**Q: Comment ajouter une nouvelle langue ?**
R: Suivez les instructions dans la section "Support Multilingue" ci-dessus.

**Q: L'application fonctionne-t-elle hors ligne ?**
R: Oui, l'application peut collecter des feedbacks hors ligne et les synchroniser automatiquement.

**Q: Comment personnaliser les conditions médicales ?**
R: Modifiez la liste `medicalConditions` dans `components/feedback-form.tsx`.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Douala General Hospital** pour la collaboration
- **Communauté open source** pour les outils utilisés
- **Locuteurs natifs** pour la validation des traductions
- **Équipe de développement** pour leur dévouement

---

**Version** : 1.0.0  
**Dernière mise à jour** : Janvier 2025  
**Développé avec ❤️ pour Douala General Hospital**