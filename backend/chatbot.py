"""
Core chatbot functionality using Hugging Face transformers
Handles model loading, response generation, and conversation management
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import asyncio
import json
import logging
from datetime import datetime

from .models import Conversation, MedicalKnowledge
from .language_adapter import LanguageAdapter
from .config import settings

logger = logging.getLogger(__name__)

class MedicalChatbot:
    """
    Main chatbot class handling medical conversations
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.model_loaded = False
        self.language_adapter = LanguageAdapter()
        
        # Medical context prompts for different scenarios
        self.medical_prompts = {
            "diagnostic": """Tu es un assistant médical bienveillant travaillant dans un contexte africain. 
            Réponds aux questions sur les symptômes avec empathie et clarté. 
            IMPORTANT: Recommande TOUJOURS de consulter un professionnel de santé. 
            Adapte tes réponses au contexte culturel local.""",
            
            "medication": """Tu es un assistant médical spécialisé dans les médicaments. 
            Fournis des informations claires sur les médicaments en tenant compte des ressources disponibles en Afrique. 
            Rappelle l'importance de suivre les prescriptions médicales.""",
            
            "care": """Tu es un assistant médical donnant des conseils de soins. 
            Fournis des conseils pratiques adaptés aux ressources disponibles localement. 
            Sois empathique et respectueux des traditions locales."""
        }
    
    async def load_model(self):
        """
        Load the language model and tokenizer
        """
        if self.model_loaded:  # Éviter de recharger inutilement
            return
    
        try:
            logger.info(f"Loading model: {settings.MODEL_NAME}")
            

            # Configuration pour les connexions lentes
            model_kwargs = {
                "token": settings.HF_API_TOKEN,
                "device_map": "auto" if torch.cuda.is_available() else None,
                "low_cpu_mem_usage": True,
                "resume_download": True,
                "timeout": 30  # Timeout augmenté
            }

            # Adapter en fonction des capacités matérielles
            if torch.cuda.is_available():
                model_kwargs.update({
                    "torch_dtype": torch.float16,
                    "load_in_8bit": True
                })

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.MODEL_NAME,
                #token=settings.HF_API_TOKEN
                **model_kwargs
            )
            
            # Load model with optimizations for resource constraints
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.MODEL_NAME,
                token=settings.HF_API_TOKEN,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                load_in_8bit=True , # Quantization for memory efficiency
                resume_download=True ,
                timeout =10,
                low_cpu_mem_usage = True

            )
            
            # Create pipeline for easier inference
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                top_p=settings.TOP_P,
                do_sample=True,
                batch_size =1
            )
            
            self.model_loaded = True
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def classify_message_type(self, message: str) -> str:
        """
        Classify the type of medical query
        """
        message_lower = message.lower()
        
        # Keywords for different categories
        diagnostic_keywords = ['symptômes', 'douleur', 'mal', 'fièvre', 'diagnostic']
        medication_keywords = ['médicament', 'pilule', 'traitement', 'posologie']
        care_keywords = ['soins', 'comment', 'prendre soin', 'conseils']
        
        if any(keyword in message_lower for keyword in diagnostic_keywords):
            return "diagnostic"
        elif any(keyword in message_lower for keyword in medication_keywords):
            return "medication"
        elif any(keyword in message_lower for keyword in care_keywords):
            return "care"
        else:
            return "general"
    
    async def generate_response(
        self,
        message: str,
        language: str = "fr",
        history: List[Dict] = None,
        user_context: Dict = None
    ) -> str:
        """
        Generate response to user message
        """
        if not self.model_loaded:
            await self.load_model()
        
        try:
            # Classify message type
            message_type = self.classify_message_type(message)
            
            # Get appropriate prompt
            system_prompt = self.medical_prompts.get(message_type, self.medical_prompts["diagnostic"])
            
            # Adapt message to target language if needed
            adapted_message = await self.language_adapter.adapt_message(message, language)
            
            # Build conversation context
            context = self._build_conversation_context(history, user_context)
            
            # Create full prompt
            full_prompt = f"{system_prompt}\n\n{context}\nUtilisateur: {adapted_message}\nAssistant:"
            
            # Generate response
            response = await self._generate_with_pipeline(full_prompt)
            
            # Post-process response
            response = self._post_process_response(response, language)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._get_fallback_response(language)
    
    async def _generate_with_pipeline(self, prompt: str) -> str:
        """
        Generate response using the pipeline
        """
        try:
            # Run inference
            result = self.pipeline(
                prompt,
                max_new_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                top_p=settings.TOP_P,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract generated text
            generated_text = result[0]['generated_text']
            
            # Extract only the assistant's response
            response_start = generated_text.find("Assistant:") + len("Assistant:")
            response = generated_text[response_start:].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error in pipeline generation: {str(e)}")
            raise
    
    def _build_conversation_context(self, history: List[Dict], user_context: Dict) -> str:
        """
        Build conversation context from history and user information
        """
        context = ""
        
        # Add user context if available
        if user_context:
            context += f"Contexte utilisateur: {json.dumps(user_context, ensure_ascii=False)}\n"
        
        # Add recent conversation history
        if history:
            context += "Historique récent:\n"
            for item in history[-3:]:  # Last 3 exchanges
                context += f"U: {item['message']}\nA: {item['response']}\n"
        
        return context
    
    def _post_process_response(self, response: str, language: str) -> str:
        """
        Post-process the generated response
        """
        # Remove any unwanted patterns
        response = response.replace("Assistant:", "").strip()
        
        # Ensure the response ends with appropriate medical disclaimer
        disclaimer = {
            "fr": "\n\n⚠️ Important: Cette information ne remplace pas une consultation médicale. Consultez un professionnel de santé pour un diagnostic précis.",
            "en": "\n\n⚠️ Important: This information does not replace medical consultation. Consult a healthcare professional for accurate diagnosis.",
        }
        
        if not any(word in response.lower() for word in ['consulter', 'médecin', 'professionnel']):
            response += disclaimer.get(language, disclaimer["fr"])
        
        return response
    
    def _get_fallback_response(self, language: str) -> str:
        """
        Get fallback response in case of errors
        """
        fallback_responses = {
            "fr": "Je suis désolé, je ne peux pas répondre à cette question pour le moment. Veuillez consulter un professionnel de santé.",
            "en": "I'm sorry, I cannot answer this question at the moment. Please consult a healthcare professional.",
        }
        return fallback_responses.get(language, fallback_responses["fr"])
    
    def get_conversation_history(self, db: Session, user_id: str, session_id: str) -> List[Dict]:
        """
        Retrieve conversation history from database
        """
        conversations = db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.session_id == session_id
        ).order_by(Conversation.timestamp.desc()).limit(10).all()
        
        history = []
        for conv in conversations:
            history.append({
                "message": conv.message,
                "response": conv.response,
                "timestamp": conv.timestamp.isoformat(),
                "language": conv.language
            })
        
        return history[::-1]  # Reverse to get chronological order
    
    def save_conversation(
        self,
        db: Session,
        user_id: str,
        session_id: str,
        message: str,
        response: str,
        language: str,
        evaluation_score: float
    ):
        """
        Save conversation to database
        """
        conversation = Conversation(
            user_id=user_id,
            session_id=session_id,
            message=message,
            response=response,
            language=language,
            evaluation_score=evaluation_score,
            is_encrypted=settings.ENCRYPT_CONVERSATIONS
        )
        
        db.add(conversation)
        db.commit()
    
    def delete_conversation_history(self, db: Session, user_id: str, session_id: str):
        """
        Delete conversation history for privacy
        """
        db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.session_id == session_id
        ).delete()
        db.commit()