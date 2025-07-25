"""
Privacy and data protection utilities
"""

from cryptography.fernet import Fernet
import os
import base64
from .config import settings

# Generate or load encryption key
def get_encryption_key():
    """Get or generate encryption key"""
    key_file = "encryption.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
    return key

# Initialize encryption
encryption_key = get_encryption_key()
cipher_suite = Fernet(encryption_key)

def encrypt_message(message: str) -> str:
    """Encrypt a message"""
    if not settings.ENCRYPT_CONVERSATIONS:
        return message
    
    try:
        encrypted_message = cipher_suite.encrypt(message.encode())
        return base64.urlsafe_b64encode(encrypted_message).decode()
    except Exception:
        return message

def decrypt_message(encrypted_message: str) -> str:
    """Decrypt a message"""
    if not settings.ENCRYPT_CONVERSATIONS:
        return encrypted_message
    
    try:
        encrypted_data = base64.urlsafe_b64decode(encrypted_message.encode())
        decrypted_message = cipher_suite.decrypt(encrypted_data)
        return decrypted_message.decode()
    except Exception:
        return encrypted_message