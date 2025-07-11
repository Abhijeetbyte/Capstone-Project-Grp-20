from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os

def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derives AES key using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # AES-256
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(master_password.encode())

def decrypt(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypts using AES-CBC without checking if result is valid."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted  # whatever is output, no verification

# Example Usage
# encrypted_data, salt, iv are fetched from the database
# master_password is what user entered (correct or incorrect)
salt_from_db = b'...'     # fetched
iv_from_db = b'...'       # fetched
encrypted_password_from_db = b'...'  # fetched

entered_master_password = input("Enter master password: ")

# Derive AES key
key = derive_key(entered_master_password, salt_from_db)

# Decrypt
decrypted_password = decrypt(encrypted_password_from_db, key, iv_from_db)

print("Decrypted Password (may be wrong):", decrypted_password.decode(errors='ignore'))
