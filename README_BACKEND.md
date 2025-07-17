# README – API de Prédiction de Sentiments

## Description
Cette API permet de prédire le sentiment d’un texte donné. Elle expose un endpoint HTTP POST qui reçoit un texte et retourne une prédiction avec un label (Négatif, Neutre, Positif).

---

## 🚀 Présentation technique
- **Framework** : Django + Django REST Framework
- **Modèle NLP** : XLM-Roberta (PyTorch, Hugging Face)
- **Langues supportées** : Français, anglais, etc.

---

## ⚙️ Prérequis & Installation
- Python 3.8+
- pip
- PyTorch
- transformers
- Django
- djangorestframework

> Installer les dépendances :
```sh
pip install -r requirements.txt
```

> Lancer le serveur :
```sh
cd sentiment_project
python manage.py runserver
```

---

## URL de base
```
http://127.0.0.1:8000/api/
```

---

## Endpoint principal
### POST `/predict/`
Permet d’envoyer un texte et d’obtenir la prédiction du sentiment.

#### Requête
- **Content-Type** : `application/json`
- **Corps JSON** :
```json
{
  "text": "Votre texte à analyser ici"
}
```

#### Réponse
- **Code HTTP** : 200 si succès, 400 si erreur de données
- **Corps JSON** :
```json
{
  "sentiment": <int>,
  "label": "<str>"
}
```
- **Exemple** :
```json
{
  "sentiment": 2,
  "label": "Positif"
}
```

#### Valeurs possibles pour `sentiment` et `label` :
| sentiment (int) | label    |
|-----------------|----------|
| 0               | Négatif  |
| 1               | Neutre   |
| 2               | Positif  |

#### Exemple avec curl
```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"text": "J’adore ce produit !"}'
```

---

## 📚 Autres endpoints
- **GET `/` ou `/api/`** : Message de bienvenue
  - Réponse :
    ```json
    { "message": "Hello Bro, ici AICELL. Bienvenue sur l'API de prédiction de sentiments !" }
    ```

---

## 🗂️ Structure du projet
- `sentiment/` : App principale (views, urls, serializers)
- `sentiment_project/` : Config Django
- `serengeti_full_model.pt` : Modèle NLP (PyTorch)

---

## 🤝 Conseils pour le frontend
- Toujours envoyer le texte dans le champ `text` (POST JSON)
- Gérer les erreurs HTTP 400 (ex : champ manquant ou mauvais format)
- Afficher le label retourné à l’utilisateur
- L’API est rapide mais le modèle peut prendre 1-2 secondes à répondre

---

## 📝 Notes
- L’API attend une requête POST avec un JSON contenant la clé `text`.
- En cas d’erreur de format ou de donnée manquante, elle retourne un code 400.
- Le serveur doit tourner (via `python manage.py runserver`) pour que l’API soit accessible.
- Le modèle fonctionne en local, la prédiction est faite via PyTorch et le tokenizer XLM-Roberta.

---

## 👨‍💻 Contact
- Projet Hackathon IA Santé 2025 – Équipe AICELLGI
- Pour toute question technique, voir le dépôt principal ou contacter l’équipe. 