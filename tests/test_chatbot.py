"""
Tests for the medical chatbot functionality
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from backend.chatbot import MedicalChatbot
from backend.evaluation import evaluate_response

@pytest.fixture
def chatbot():
    """Create a chatbot instance for testing"""
    return MedicalChatbot()

@pytest.fixture
def mock_db():
    """Create a mock database session"""
    return Mock()

class TestMedicalChatbot:
    """Test cases for the medical chatbot"""
    
    def test_classify_message_type(self, chatbot):
        """Test message classification"""
        # Test diagnostic classification
        assert chatbot.classify_message_type("J'ai de la fièvre") == "diagnostic"
        assert chatbot.classify_message_type("Mes symptômes sont...") == "diagnostic"
        
        # Test medication classification
        assert chatbot.classify_message_type("Quel médicament prendre?") == "medication"
        assert chatbot.classify_message_type("Posologie du paracétamol") == "medication"
        
        # Test care classification
        assert chatbot.classify_message_type("Comment soigner...") == "care"
        assert chatbot.classify_message_type("Conseils pour...") == "care"
    
    def test_build_conversation_context(self, chatbot):
        """Test conversation context building"""
        history = [
            {"message": "J'ai mal", "response": "Où avez-vous mal?"},
            {"message": "À la tête", "response": "Depuis quand?"}
        ]
        
        user_context = {"age": 30, "gender": "Homme"}
        
        context = chatbot._build_conversation_context(history, user_context)
        
        assert "age" in context
        assert "J'ai mal" in context
        assert "À la tête" in context
    
    def test_post_process_response(self, chatbot):
        """Test response post-processing"""
        response = "Vous devriez prendre du repos."
        processed = chatbot._post_process_response(response, "fr")
        
        # Should add medical disclaimer
        assert "consulter" in processed.lower() or "professionnel" in processed.lower()
    
    def test_get_fallback_response(self, chatbot):
        """Test fallback responses"""
        fallback_fr = chatbot._get_fallback_response("fr")
        fallback_en = chatbot._get_fallback_response("en")
        
        assert "désolé" in fallback_fr.lower()
        assert "sorry" in fallback_en.lower()

class TestResponseEvaluation:
    """Test cases for response evaluation"""
    
    def test_evaluate_empathy(self):
        """Test empathy evaluation"""
        # High empathy response
        response = "Je comprends votre inquiétude. C'est important de prendre soin de vous."
        evaluation = evaluate_response("J'ai peur", response)
        
        assert evaluation['empathy_score'] > 0.3
    
    def test_evaluate_safety(self):
        """Test safety evaluation"""
        # Safe response with medical disclaimer
        response = "Consultez un médecin pour un diagnostic précis."
        evaluation = evaluate_response("J'ai mal", response)
        
        assert evaluation['safety_score'] > 0.8
        
        # Unsafe response (too definitive)
        unsafe_response = "C'est sûrement une grippe, pas besoin de consulter."
        evaluation = evaluate_response("J'ai de la fièvre", unsafe_response)
        
        assert evaluation['safety_score'] < 0.7
    
    def test_generate_suggestions(self):
        """Test suggestion generation"""
        evaluation = evaluate_response("J'ai de la fièvre", "Vous devriez consulter.")
        
        suggestions = evaluation.get('suggestions', [])
        assert len(suggestions) > 0
        assert any('température' in s.lower() for s in suggestions)

@pytest.mark.asyncio
class TestAsyncFunctionality:
    """Test asynchronous functionality"""
    
    async def test_language_adaptation(self):
        """Test language adaptation"""
        from backend.language_adapter import LanguageAdapter
        
        adapter = LanguageAdapter()
        
        # Test basic adaptation
        adapted = await adapter.adapt_message("Hello", "fr")
        assert adapted is not None
    
    @patch('backend.chatbot.MedicalChatbot._generate_with_pipeline')
    async def test_generate_response(self, mock_generate, chatbot):
        """Test response generation"""
        # Mock the pipeline response
        mock_generate.return_value = "Consultez un médecin pour vos symptômes."
        
        # Test response generation
        response = await chatbot.generate_response(
            message="J'ai mal à la tête",
            language="fr"
        )
        
        assert response is not None
        assert "médecin" in response.lower()

def test_medical_knowledge_loading():
    """Test loading of medical knowledge"""
    import json
    
    # Test loading medical knowledge data
    with open('data/medical_knowledge.json', 'r', encoding='utf-8') as f:
        knowledge = json.load(f)
    
    assert 'conditions' in knowledge
    assert 'medications' in knowledge
    assert len(knowledge['conditions']) > 0
    
    # Test condition structure
    condition = knowledge['conditions'][0]
    assert 'symptoms' in condition
    assert 'treatment' in condition
    assert 'cultural_context' in condition

def test_conversation_data_loading():
    """Test loading of test conversation data"""
    import json
    
    # Test loading test conversations
    with open('data/test_conversations.json', 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    assert 'test_conversations' in conversations
    assert 'evaluation_criteria' in conversations
    assert len(conversations['test_conversations']) > 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])