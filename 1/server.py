import socket
import threading

# Paramètres du serveur
HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau
PORT = 12345       # Port du serveur

# Liste des clients connectés
clients = []

# Fonction pour gérer la réception et la diffusion des messages
def handle_client(client_socket, address):
    print(f"[NOUVELLE CONNEXION] {address} connecté.")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[MESSAGE] {address}: {message}")
            broadcast(message, client_socket)
    except:
        pass
    finally:
        print(f"[DÉCONNEXION] {address} déconnecté.")
        clients.remove(client_socket)
        client_socket.close()

# Fonction pour envoyer un message à tous les clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Démarrage du serveur
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[DÉMARRAGE] Serveur en écoute sur {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
