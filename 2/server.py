import socket
import threading
from crypto import cesar_encrypt, cesar_decrypt, vigenere_encrypt, vigenere_decrypt

# Configuration
HOST = '0.0.0.0'
PORT = 12345
clients = []

# Clé de chiffrement (à partager avec les clients)
CIPHER_KEY = "SECRET"

def handle_client(client_socket, address):
    print(f"[NOUVELLE CONNEXION] {address} connecté.")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # Déchiffrement du message avant affichage
            decrypted_message = vigenere_decrypt(message, CIPHER_KEY)
            print(f"[MESSAGE] {address}: {decrypted_message}")
            
            # Réémission après chiffrement
            broadcast(message, client_socket)
    except:
        pass
    finally:
        print(f"[DÉCONNEXION] {address} déconnecté.")
        clients.remove(client_socket)
        client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def start_server():
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
