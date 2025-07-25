"""
Response evaluation and quality assessment
"""

import re
from typing import Dict, List
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class ResponseEvaluator:
    """
    Evaluates the quality and appropriateness of chatbot responses
    """
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Keywords that indicate good medical responses
        self.positive_indicators = [
            'consulter', 'médecin', 'professionnel', 'diagnostic',
            'traitement', 'suivi', 'important', 'attention'
        ]
        
        # Keywords that might indicate problematic responses
        self.negative_indicators = [
            'certain', 'sûr', 'définitivement', 'toujours',
            'jamais', 'impossible', 'pas besoin'
        ]
    
    def evaluate_response(self, user_message: str, bot_response: str) -> Dict:
        """
        Evaluate a bot response across multiple dimensions
        """
        evaluation = {
            'score': 0.0,
            'confidence': 0.0,
            'empathy_score': 0.0,
            'safety_score': 0.0,
            'cultural_appropriateness': 0.0,
            'suggestions': []
        }
        
        # Evaluate empathy
        evaluation['empathy_score'] = self._evaluate_empathy(bot_response)
        
        # Evaluate safety
        evaluation['safety_score'] = self._evaluate_safety(bot_response)
        
        # Evaluate cultural appropriateness
        evaluation['cultural_appropriateness'] = self._evaluate_cultural_appropriateness(bot_response)
        
        # Calculate overall score
        evaluation['score'] = (
            evaluation['empathy_score'] * 0.3 +
            evaluation['safety_score'] * 0.5 +
            evaluation['cultural_appropriateness'] * 0.2
        )
        
        # Generate suggestions
        evaluation['suggestions'] = self._generate_suggestions(user_message, bot_response)
        
        # Set confidence based on score
        evaluation['confidence'] = min(evaluation['score'] + 0.1, 1.0)
        
        return evaluation
    
    def _evaluate_empathy(self, response: str) -> float:
        """
        Evaluate empathy level of the response
        """
        empathy_words = [
            'comprends', 'désolé', 'inquiet', 'préoccupé',
            'important', 'prendre soin', 'soutien', 'aide'
        ]
        
        empathy_score = 0.0
        response_lower = response.lower()
        
        # Check for empathetic language
        for word in empathy_words:
            if word in response_lower:
                empathy_score += 0.1
        
        # Check sentiment
        sentiment = self.sentiment_analyzer.polarity_scores(response)
        if sentiment['compound'] >= 0.1:  # Positive sentiment
            empathy_score += 0.2
        
        return min(empathy_score, 1.0)
    
    def _evaluate_safety(self, response: str) -> float:
        """
        Evaluate safety of the medical advice
        """
        safety_score = 0.8  # Start with high safety score
        response_lower = response.lower()
        
        # Check for medical disclaimer
        if any(word in response_lower for word in ['consulter', 'médecin', 'professionnel']):
            safety_score += 0.2
        
        # Penalize overconfident statements
        for negative_indicator in self.negative_indicators:
            if negative_indicator in response_lower:
                safety_score -= 0.1
        
        # Reward cautious language
        for positive_indicator in self.positive_indicators:
            if positive_indicator in response_lower:
                safety_score += 0.05
        
        return max(min(safety_score, 1.0), 0.0)
    
    def _evaluate_cultural_appropriateness(self, response: str) -> float:
        """
        Evaluate cultural appropriateness for African context
        """
        cultural_score = 0.7  # Base score
        response_lower = response.lower()
        
        # Check for cultural sensitivity
        cultural_indicators = [
            'local', 'traditionnel', 'culturel', 'communauté',
            'famille', 'respecter', 'comprendre'
        ]
        
        for indicator in cultural_indicators:
            if indicator in response_lower:
                cultural_score += 0.1
        
        # Check for inappropriate assumptions
        inappropriate_terms = [
            'toujours disponible', 'facilement accessible',
            'cher', 'coûteux'
        ]
        
        for term in inappropriate_terms:
            if term in response_lower:
                cultural_score -= 0.1
        
        return max(min(cultural_score, 1.0), 0.0)
    
    def _generate_suggestions(self, user_message: str, bot_response: str) -> List[str]:
        """
        Generate follow-up suggestions based on the conversation
        """
        suggestions = []
        
        # Analyze user message to generate relevant suggestions
        message_lower = user_message.lower()
        
        if 'fièvre' in message_lower or 'température' in message_lower:
            suggestions.extend([
                "Quelle est votre température exacte?",
                "Avez-vous d'autres symptômes?",
                "Depuis combien de temps avez-vous de la fièvre?"
            ])
        
        if 'douleur' in message_lower or 'mal' in message_lower:
            suggestions.extend([
                "Pouvez-vous décrire la douleur?",
                "Où exactement ressentez-vous la douleur?",
                "La douleur est-elle constante ou intermittente?"
            ])
        
        if 'médicament' in message_lower:
            suggestions.extend([
                "Prenez-vous d'autres médicaments?",
                "Avez-vous des allergies médicamenteuses?",
                "Quelle est la posologie prescrite?"
            ])
        
        return suggestions[:3]  # Limit to 3 suggestions

# Global evaluator instance
evaluator = ResponseEvaluator()

def evaluate_response(user_message: str, bot_response: str) -> Dict:
    """
    Evaluate a response using the global evaluator
    """
    return evaluator.evaluate_response(user_message, bot_response)