"""
Streamlit frontend for the African Medical Chatbot
Alternative interface for users who prefer Streamlit
"""

import streamlit as st
import requests
import json
import uuid
from datetime import datetime
from streamlit_chat import message
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_BASE_URL = "http://localhost:8000"
SUPPORTED_LANGUAGES = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "wolof": "🇸🇳 Wolof",
    "hausa": "🇳🇬 Hausa",
    "swahili": "🇰🇪 Swahili"
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_context" not in st.session_state:
    st.session_state.user_context = {}

def authenticate_user():
    """Authenticate user with the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/token",
            data={"username": "demo_user", "password": "demo_password"}
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            st.error("Erreur d'authentification")
            return None
    except Exception as e:
        st.error(f"Erreur de connexion: {str(e)}")
        return None

def send_message(message_text, language):
    """Send message to the chatbot API"""
    if not st.session_state.access_token:
        st.session_state.access_token = authenticate_user()
    
    if not st.session_state.access_token:
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "message": message_text,
            "language": language,
            "session_id": st.session_state.session_id,
            "user_context": st.session_state.user_context
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Erreur lors de l'envoi: {str(e)}")
        return None

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Assistant Médical Africain",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #2E8B57 0%, #32CD32 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: #007bff;
        color: white;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: right;
    }
    
    .bot-message {
        background: #28a745;
        color: white;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Assistant Médical Africain</h1>
        <p>Votre assistant de santé bienveillant et culturellement adapté</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Language selection
        selected_language = st.selectbox(
            "Langue / Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: SUPPORTED_LANGUAGES[x],
            index=0
        )
        
        # User context
        st.subheader("📋 Informations utilisateur")
        age = st.number_input("Âge", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Sexe", ["Non spécifié", "Homme", "Femme", "Autre"])
        location = st.text_input("Localisation", placeholder="Ville, Pays")
        
        # Update user context
        st.session_state.user_context = {
            "age": age,
            "gender": gender,
            "location": location
        }
        
        # Warning disclaimer
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Avertissement Important</strong><br>
            Cet assistant ne remplace pas une consultation médicale. 
            En cas d'urgence, contactez immédiatement un professionnel de santé.
        </div>
        """, unsafe_allow_html=True)
        
        # Clear conversation button
        if st.button("🗑️ Effacer la conversation"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
    
    # Main chat interface
    st.subheader("💬 Conversation")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                message(msg["content"], is_user=True, key=f"user_{i}")
            else:
                message(msg["content"], is_user=False, key=f"bot_{i}")
    
    # Chat input
    user_input = st.chat_input("Tapez votre message ici...")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Send message to API
        with st.spinner("L'assistant réfléchit..."):
            response = send_message(user_input, selected_language)
        
        if response:
            # Add bot response to history
            bot_response = response["response"]
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            # Display suggestions if available
            if response.get("suggestions"):
                st.subheader("💡 Questions suggérées")
                for suggestion in response["suggestions"]:
                    if st.button(suggestion, key=f"suggestion_{len(st.session_state.messages)}_{suggestion}"):
                        st.session_state.messages.append({"role": "user", "content": suggestion})
                        with st.spinner("L'assistant réfléchit..."):
                            suggestion_response = send_message(suggestion, selected_language)
                        if suggestion_response:
                            st.session_state.messages.append({"role": "assistant", "content": suggestion_response["response"]})
                        st.rerun()
        
        # Refresh to show new messages
        st.rerun()
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🌍 Assistant Médical Africain - Développé avec ❤️ pour l'Afrique</p>
        <p><small>Version 1.0 - Open Source</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()