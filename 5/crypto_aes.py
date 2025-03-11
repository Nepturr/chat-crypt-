from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def generate_aes_key():
    """ Génère une clé AES de 256 bits """
    return os.urandom(32)  # 256 bits (32 bytes)

def pad(data):
    """ Ajoute du padding pour que les données soient un multiple de 16 bytes """
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length] * padding_length)

def unpad(data):
    """ Supprime le padding """
    padding_length = data[-1]
    return data[:-padding_length]

def aes_encrypt(plaintext, key):
    """ Chiffre un texte avec AES en mode CBC """
    iv = os.urandom(16)  # Vecteur d'initialisation aléatoire
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padded_text = pad(plaintext.encode())
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    
    return base64.b64encode(iv + ciphertext).decode()  # Encodage en base64

def aes_decrypt(ciphertext, key):
    """ Déchiffre un texte AES en CBC """
    raw_data = base64.b64decode(ciphertext)
    iv = raw_data[:16]
    encrypted_message = raw_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded_text = decryptor.update(encrypted_message) + decryptor.finalize()
    return unpad(decrypted_padded_text).decode()
