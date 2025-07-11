import sqlite3
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_password(password, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()
    return encrypted_password, iv

def insert_credential(service, username, password):
    # Derive encryption key (example - use PBKDF2)
    key = b'examplekey1234567890abcdef'  # Replace with actual key derivation logic

    # Encrypt password
    encrypted_password, iv = encrypt_password(password, key)
    
    # Insert into DB
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO credentials (service, username, password, iv, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (service, username, encrypted_password, iv, '2025-04-26 00:00:00'))  # Use current timestamp here
    conn.commit()
    conn.close()
