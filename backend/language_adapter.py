"""
Language adaptation and translation module
Handles multilingual support and cultural context adaptation
"""

from googletrans import Translator
from langdetect import detect
import logging
from typing import Dict, List
import asyncio

logger = logging.getLogger(__name__)

class LanguageAdapter:
    """
    Handles language detection, translation, and cultural adaptation
    """
    
    def __init__(self):
        self.translator = Translator()
        
        # Cultural adaptation patterns for African context
        self.cultural_adaptations = {
            "fr": {
                "greetings": ["Bonjour", "Bonsoir", "Salut"],
                "respectful_terms": ["Monsieur", "Madame", "Docteur"],
                "local_remedies": {
                    "fever": "En plus du traitement médical, vous pouvez boire des tisanes à base de citron et gingembre.",
                    "stomach": "Les tisanes à base de menthe peuvent aider, mais consultez un médecin.",
                    "headache": "Reposez-vous dans un endroit calme et frais."
                }
            },
            "wolof": {
                "greetings": ["Asalaa maalekum", "Nanga def"],
                "respectful_terms": ["Boroom", "Yaay"],
                "cultural_notes": "Tenir compte des pratiques traditionnelles de guérison"
            },
            "hausa": {
                "greetings": ["Sannu", "Barka da safe"],
                "respectful_terms": ["Malam", "Hajiya"],
                "cultural_notes": "Respecter les pratiques religieuses dans les soins"
            }
        }
    
    async def adapt_message(self, message: str, target_language: str) -> str:
        """
        Adapt message to target language and cultural context
        """
        try:
            # Detect source language
            source_lang = detect(message)
            
            # If message is already in target language, return as-is
            if source_lang == target_language:
                return message
            
            # Translate if needed
            if target_language in ['fr', 'en']:
                translated = self.translator.translate(
                    message, 
                    src=source_lang, 
                    dest=target_language
                ).text
                return translated
            
            # For local languages, provide basic cultural adaptation
            return self._adapt_to_local_culture(message, target_language)
            
        except Exception as e:
            logger.error(f"Error adapting message: {str(e)}")
            return message
    
    def _adapt_to_local_culture(self, message: str, language: str) -> str:
        """
        Adapt message to local cultural context
        """
        # Basic cultural adaptation - in practice, would use specialized models
        cultural_context = self.cultural_adaptations.get(language, {})
        
        # Add appropriate greeting if not present
        if not any(greeting.lower() in message.lower() 
                  for greeting in cultural_context.get("greetings", [])):
            greeting = cultural_context.get("greetings", ["Bonjour"])[0]
            message = f"{greeting}! {message}"
        
        return message
    
    def get_cultural_health_advice(self, condition: str, language: str) -> str:
        """
        Get culturally appropriate health advice
        """
        cultural_context = self.cultural_adaptations.get(language, {})
        local_remedies = cultural_context.get("local_remedies", {})
        
        return local_remedies.get(condition, "")
    
    def translate_medical_terms(self, terms: List[str], target_language: str) -> Dict[str, str]:
        """
        Translate medical terms to target language
        """
        translations = {}
        
        try:
            for term in terms:
                if target_language in ['fr', 'en']:
                    translation = self.translator.translate(
                        term, 
                        dest=target_language
                    ).text
                    translations[term] = translation
                else:
                    # For local languages, provide basic translations
                    translations[term] = self._get_local_medical_term(term, target_language)
            
        except Exception as e:
            logger.error(f"Error translating medical terms: {str(e)}")
        
        return translations
    
    def _get_local_medical_term(self, term: str, language: str) -> str:
        """
        Get local language equivalent for medical terms
        """
        # Basic medical term translations (would be expanded with proper linguistic resources)
        medical_translations = {
            "wolof": {
                "fever": "tang",
                "headache": "bopp bu yar",
                "stomach": "biir"
            },
            "hausa": {
                "fever": "zazzabi",
                "headache": "ciwon kai",
                "stomach": "ciki"
            }
        }
        
        return medical_translations.get(language, {}).get(term.lower(), term)