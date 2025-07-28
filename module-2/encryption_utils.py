from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    """Generate a Fernet key from password using SHA256"""
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_file(data: bytes, password: str) -> bytes:
    key = generate_key(password)
    return Fernet(key).encrypt(data)

def decrypt_file(encrypted_data: bytes, password: str) -> bytes:
    key = generate_key(password)
    return Fernet(key).decrypt(encrypted_data)
