import socket
import threading

# Paramètres du serveur
SERVER_HOST = '127.0.0.1'  # Adresse du serveur (mettre l'IP du serveur si distant)
SERVER_PORT = 12345        # Port du serveur

# Fonction pour recevoir les messages du serveur
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[Message reçu] {message}")
        except:
            print("[ERREUR] Connexion perdue.")
            break

# Démarrage du client
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[CONNECTÉ] Connecté au serveur.")
    except:
        print("[ERREUR] Impossible de se connecter au serveur.")
        return

    # Lancement du thread pour recevoir les messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Envoi des messages
    try:
        while True:
            message = input("Vous: ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
    except:
        pass
    finally:
        print("[DÉCONNEXION] Fermeture de la connexion.")
        client_socket.close()

if __name__ == "__main__":
    start_client()
