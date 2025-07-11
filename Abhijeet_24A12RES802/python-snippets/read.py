def decrypt_password(encrypted_password, iv, key):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted_password) + decryptor.finalize()
    return decrypted_password.decode()

def read_credential(service, username):
    # Derive encryption key
    key = b'examplekey1234567890abcdef'
    
    # Fetch encrypted password and IV from DB
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password, iv FROM credentials WHERE service = ? AND username = ?
    ''', (service, username))
    result = cursor.fetchone()
    
    if result:
        encrypted_password, iv = result
        decrypted_password = decrypt_password(encrypted_password, iv, key)
        return decrypted_password
    else:
        return None
