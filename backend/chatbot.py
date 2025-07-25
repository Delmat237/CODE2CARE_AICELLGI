import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sqlalchemy.orm import Session
from typing import List, Dict
import json
import logging

from .models import Conversation
from .language_adapter import LanguageAdapter
from .config import settings

logger = logging.getLogger(__name__)

from transformers import AutoTokenizer, AutoModelForCausalLM

class MedicalChatbot:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False

    async def load_model(self):
        try:
            model_path = "C:\\Users\\JUNIOR\\Desktop\\personnel\\aicell\\CODE2CARE_AICELLGI\\tinyllama-lora-checkpoint"  # 🔁 Mets ici ton chemin exact
            print(f"📦 Chargement du modèle depuis : {model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # ou torch.float16 si tu forces FP16
                device_map="auto"
            )
            self.model.eval()
            self.model_loaded = True
            print("✅ Modèle chargé avec succès.")
        except Exception as e:
            print("❌ Erreur de chargement du modèle :", str(e))
            self.model_loaded = False


    def classify_message_type(self, message: str) -> str:
        message = message.lower()
        if any(k in message for k in ['symptômes', 'fièvre', 'douleur']): return "diagnostic"
        if any(k in message for k in ['médicament', 'traitement', 'pilule']): return "medication"
        if any(k in message for k in ['soins', 'prendre soin']): return "care"
        return "diagnostic"

    async def generate_response(self, message: str, language: str = "fr", history: List[Dict] = None, user_context: Dict = None) -> str:
        if not self.model_loaded:
            await self.load_model()

        try:
            prompt_type = self.classify_message_type(message)
            system_prompt = self.medical_prompts.get(prompt_type, self.medical_prompts["diagnostic"])

            adapted_message = await self.language_adapter.adapt_message(message, language)
            context = self._build_context(history, user_context)

            full_prompt = f"{system_prompt}\n{context}\nUtilisateur: {adapted_message}\nAssistant:"
            result = self.pipeline(
                full_prompt,
                max_new_tokens=200,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response = result[0]["generated_text"].split("Assistant:")[-1].strip()
            return self._post_process_response(response, language)
        except Exception as e:
            logger.error(f"Erreur de génération : {e}")
            return "Je suis désolé, je n’ai pas compris. Veuillez réessayer."

    def _build_context(self, history: List[Dict], user_context: Dict) -> str:
        context = ""
        if user_context:
            context += f"Contexte utilisateur : {json.dumps(user_context, ensure_ascii=False)}\n"
        if history:
            context += "Historique :\n"
            for h in history[-3:]:
                context += f"U: {h['message']}\nA: {h['response']}\n"
        return context

    def _post_process_response(self, response: str, language: str) -> str:
        disclaimer = {
            "fr": "\n⚠️ Ceci ne remplace pas une consultation médicale.",
            "en": "\n⚠️ This does not replace medical advice.",
        }
        if "consulte" not in response.lower():
            response += disclaimer.get(language, disclaimer["fr"])
        return response
