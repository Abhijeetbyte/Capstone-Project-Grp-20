# 1. Create: Insert New Credential
def create_credential(service, username, password):
    """
    Encrypts the password and inserts the credential into the database.
    """
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

# 2. Read: Fetch and Decrypt Credential
def read_credential(service, username):
    """
    Fetches the encrypted credential and decrypts it in memory.
    """
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

# 3. Update: Update an Existing Credential
def update_credential(service, username, new_password):
    """
    Updates an existing credential with a new password after encrypting it.
    """
    # Derive encryption key
    key = b'examplekey1234567890abcdef'
    
    # Encrypt new password
    encrypted_password, iv = encrypt_password(new_password, key)
    
    # Update the credential in the database
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE credentials
        SET password = ?, iv = ?
        WHERE service = ? AND username = ?
    ''', (encrypted_password, iv, service, username))
    conn.commit()
    conn.close()

# 4. Delete: Remove a Credential
def delete_credential(service, username):
    """
    Permanently deletes a credential from the database.
    """
    # User confirmation (this would be handled in UI)
    confirmation = input(f"Are you sure you want to delete the credential for {service} ({username})? (y/n): ")
    
    if confirmation.lower() == 'y':
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM credentials WHERE service = ? AND username = ?
        ''', (service, username))
        conn.commit()
        conn.close()
        print(f"Credential for {service} deleted.")
    else:
        print("Deletion cancelled.")
