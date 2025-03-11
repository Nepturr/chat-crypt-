import socket
import threading
import rsa
import tkinter as tk
from tkinter import scrolledtext
from crypto_aes import aes_encrypt, aes_decrypt, generate_aes_key

# Configuration du serveur
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
aes_key = None  # La clé AES sera reçue après l'échange RSA

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Sécurisé AES 🔐")
        self.root.geometry("500x500")

        # Zone d'affichage des messages
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Zone de saisie
        self.message_entry = tk.Entry(root, font=("Arial", 12))
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        # Bouton d'envoi
        self.send_button = tk.Button(root, text="Envoyer 📩", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(pady=5)

        # Connexion au serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            self.display_message("🔗 Connecté au serveur.")
            self.exchange_keys()
        except:
            self.display_message("❌ Erreur : Impossible de se connecter au serveur.")
            return

        # Thread pour recevoir les messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def exchange_keys(self):
        """ Échange la clé AES avec le serveur via RSA """
        global aes_key

        # Recevoir la clé publique RSA du serveur
        public_key_data = self.client_socket.recv(1024)
        public_key = rsa.PublicKey.load_pkcs1(public_key_data)

        # Générer une clé AES aléatoire pour le chiffrement des messages
        aes_key = generate_aes_key()

        # Chiffrer la clé AES avec la clé publique RSA du serveur
        encrypted_key = rsa.encrypt(aes_key, public_key)

        # Envoyer la clé AES chiffrée au serveur
        self.client_socket.send(encrypted_key)

        self.display_message("🔑 Clé AES échangée.")

    def display_message(self, message):
        """ Affiche un message dans la zone de discussion """
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def send_message(self, event=None):
        """ Chiffre et envoie un message """
        global aes_key

        message = self.message_entry.get()
        if message:
            encrypted_message = aes_encrypt(message, aes_key)
            self.client_socket.send(encrypted_message.encode())
            self.display_message(f"📝 Vous: {message}")
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        """ Reçoit et affiche les messages chiffrés/déchiffrés """
        global aes_key

        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break

                # Déchiffrement
                decrypted_message = aes_decrypt(message, aes_key)
                self.display_message(f"📩 {decrypted_message}")
            except:
                self.display_message("⚠️ Connexion perdue.")
                break

    def close_client(self):
        """ Ferme proprement la connexion au serveur """
        self.client_socket.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", client.close_client)  # Gère la fermeture propre de la connexion
    root.mainloop()
