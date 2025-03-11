import socket
import threading
import rsa
from crypto import vigenere_encrypt, vigenere_decrypt

# Charger la clé privée du serveur
with open("private_key.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# Charger la clé publique à envoyer aux clients
with open("public_key.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Configuration
HOST = '0.0.0.0'
PORT = 12345
clients = {}  # Stocke les sockets et clés symétriques

def broadcast(message, sender_socket):
    """ Diffuse un message chiffré aux autres clients """
    sender_key = clients[sender_socket]  # Clé du client qui envoie

    for client_socket, client_key in clients.items():
        if client_socket != sender_socket:
            try:
                # Déchiffrement du message original
                decrypted_message = vigenere_decrypt(message, sender_key)

                # Chiffrement avec la clé du destinataire
                encrypted_message = vigenere_encrypt(decrypted_message, client_key)

                # Envoi au client
                client_socket.send(encrypted_message.encode())
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket, address):
    """ Gère la communication avec un client """
    print(f"[NOUVELLE CONNEXION] {address} connecté.")

    # Envoyer la clé publique RSA au client
    client_socket.send(public_key.save_pkcs1())

    # Recevoir la clé symétrique chiffrée
    encrypted_key = client_socket.recv(256)
    symmetric_key = rsa.decrypt(encrypted_key, private_key).decode()
    clients[client_socket] = symmetric_key  # Stocker la clé

    print(f"🔑 Clé symétrique reçue de {address}: {symmetric_key}")

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Diffuser le message aux autres clients
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
    print(f"[DÉMARRAGE] Serveur sécurisé en écoute sur {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
