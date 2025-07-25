
# 🧠 Assistant Virtuel Médical - Volet 2

## 🎯 Objectif

Ce projet vise à concevoir un **chatbot médical intelligent** basé sur un **modèle de langage étendu (MLE)** tel que **Mistral** ou **LLaMA**, pour assister les patients dans la compréhension de leurs diagnostics, traitements, médicaments et recommandations de santé.

---

## 📚 Fonctionnalités principales

- 💬 Répondre aux questions des patients en langage naturel.
- 🏥 Expliquer des diagnostics et traitements à partir de **résumés cliniques**.
- 🌍 Support **multilingue** (français inclus).
- 🧩 Intégration de documents médicaux via **RAG (Retrieval-Augmented Generation)**.
- 🤖 Modèle LLM open-source exécuté localement (Mistral ou LLaMA).
- 🌐 Interface connectable à une app **React.js** ou **Flutter** via une API.

---

## 🧱 Architecture technique

1. **LangChain** orchestre la génération + recherche.
2. **FAISS** indexe les résumés cliniques sous forme vectorielle.
3. **CTransformers** exécute le modèle Mistral ou LLaMA localement.
4. **Embeddings** générés avec `sentence-transformers` (MiniLM).
5. **CSV de données cliniques** utilisé comme source médicale.

---

## 📂 Fichiers attendus

- `clinical_summaries.csv` : contient les résumés cliniques utilisés pour entraîner ou interroger le modèle.
- `main.py` : script Python principal (voir exemple plus bas).
- `requirements.txt` : dépendances Python.

---

## ▶️ Installation

### 🔧 Prérequis

- Python 3.9+
- Environnement virtuel (recommandé)
- Un GPU est optionnel (les modèles GGUF tournent en CPU)

### 📦 Installation

```bash
git clone https://github.com/votre-projet/assistant-medical.git
cd assistant-medical
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sur Windows

pip install -r requirements.txt
```

### 📜 `requirements.txt`

```txt
langchain
faiss-cpu
ctransformers
pandas
sentence-transformers
```

---

## 🧪 Exemple d’utilisation

```bash
python main.py
```

Et poser une question comme :

```
Quels sont les effets secondaires du traitement contre l'hypertension ?
```

---

## 🧠 Exemple de modèle utilisé

- **Mistral 7B Instruct** (GGUF) :  
  `TheBloke/Mistral-7B-Instruct-v0.1-GGUF`
- **LLaMA 2 Chat** (GGUF) :  
  `TheBloke/Llama-2-7B-Chat-GGUF`

Téléchargez-les depuis [HuggingFace - TheBloke](https://huggingface.co/TheBloke)

---

## 🧠 Exemple de pipeline (LangChain)

```text
Question utilisateur → Recherche documentaire (FAISS) → Prompt enrichi → Réponse générée
```

---

## 📈 Évaluation prévue

- ✅ Tests d’utilisabilité
- ✅ Évaluation par des cliniciens (qualité des réponses)
- ✅ Mesure de la clarté, empathie et pertinence médicale

---

## 🧑‍⚕️ Limites

⚠️ Ce chatbot ne **remplace pas un diagnostic médical**.  
Il fournit des explications **vulgarisées à partir de sources cliniques existantes**.

---

## 📤 Déploiement (optionnel)

- Back-end exposable avec **FastAPI**.
- Intégrable dans une app **React.js** ou **Flutter** via API REST.

---

## 📃 Licence

MIT – Utilisation libre pour la recherche ou projets à but non lucratif.

---

## 👥 Auteurs

- Ton Nom – [tonemail@example.com](mailto:tonemail@example.com)
- Projet dans le cadre du **Défi IA – Volet 2 – Éducation et soutien aux patients**
