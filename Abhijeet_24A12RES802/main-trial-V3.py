from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode
import os

def derive_key(master_password: str, salt: bytes):
    """Derives a key from the master password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode())

def encrypt_password(master_password: str, password: str):
    """Encrypt a password using AES and the master password."""
    salt = os.urandom(16)  # Salt to prevent rainbow table attacks
    key = derive_key(master_password, salt)

    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()

    return b64encode(salt + iv + encrypted_password).decode('utf-8')  # Combine and encode everything

def decrypt_password(master_password: str, encrypted_data: str):
    """Decrypt a password using AES and the master password."""
    data = b64decode(encrypted_data)
    salt, iv, encrypted_password = data[:16], data[16:32], data[32:]

    key = derive_key(master_password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    password = decryptor.update(encrypted_password) + decryptor.finalize()

    return password.decode('utf-8')

# Example usage
master_password = "secure_master_password"
password = "my_secure_password"
encrypted_password = encrypt_password(master_password, password)
print("Encrypted Password:", encrypted_password)

decrypted_password = decrypt_password(master_password, encrypted_password)
print("Decrypted Password:", decrypted_password)
