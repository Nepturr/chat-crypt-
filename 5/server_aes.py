import socket
import threading
import rsa
from crypto_aes import aes_encrypt, aes_decrypt

# Charger la clé privée RSA du serveur
with open("keys/private_key.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# Charger la clé publique
with open("keys/public_key.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Configuration
HOST = '0.0.0.0'
PORT = 12345
clients = {}  # Stocke les clients et leurs clés AES

def broadcast(message, sender_socket):
    """ Diffuse un message chiffré AES à tous les autres clients """
    sender_key = clients[sender_socket]

    for client_socket, client_key in clients.items():
        if client_socket != sender_socket:
            try:
                decrypted_message = aes_decrypt(message, sender_key)  # Déchiffrer avec la clé du sender
                encrypted_message = aes_encrypt(decrypted_message, client_key)  # Rechiffrer avec la clé du destinataire
                client_socket.send(encrypted_message.encode())
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket, address):
    """ Gère la communication avec un client """
    print(f"[NOUVELLE CONNEXION] {address} connecté.")

    # Envoyer la clé publique RSA
    client_socket.send(public_key.save_pkcs1())

    # Recevoir la clé AES chiffrée
    encrypted_key = client_socket.recv(256)
    aes_key = rsa.decrypt(encrypted_key, private_key)
    clients[client_socket] = aes_key  # Stocker la clé AES

    print(f"🔑 Clé AES reçue de {address}")

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Diffuser le message chiffré
            broadcast(message, client_socket)

    except:
        pass
    finally:
        print(f"[DÉCONNEXION] {address} déconnecté.")
        del clients[client_socket]
        client_socket.close()

def start_server():
    """ Démarre le serveur """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[DÉMARRAGE] Serveur AES en écoute sur {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
