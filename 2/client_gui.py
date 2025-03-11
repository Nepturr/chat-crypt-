import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from crypto import vigenere_encrypt, vigenere_decrypt  # Import des fonctions de chiffrement

# Configuration
SERVER_HOST = '127.0.0.1'  # Adresse du serveur
SERVER_PORT = 12345
CIPHER_KEY = "SECRET"

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Sécurisé 🔐")
        self.root.geometry("500x500")
        
        # Zone d'affichage des messages
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Zone de saisie
        self.message_entry = tk.Entry(root, font=("Arial", 12))
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)  # Permet d'envoyer avec Entrée

        # Bouton d'envoi
        self.send_button = tk.Button(root, text="Envoyer 📩", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(pady=5)

        # Démarrer la connexion au serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            self.display_message("🔗 Connecté au serveur.")
        except:
            self.display_message("❌ Erreur : Impossible de se connecter au serveur.")
            return

        # Thread pour recevoir les messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def display_message(self, message):
        """ Affiche un message dans la zone de discussion """
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def send_message(self, event=None):
        """ Envoie un message chiffré au serveur """
        message = self.message_entry.get()
        if message:
            encrypted_message = vigenere_encrypt(message, CIPHER_KEY)
            self.client_socket.send(encrypted_message.encode('utf-8'))
            self.display_message(f"📝 Vous: {message}")
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        """ Reçoit et affiche les messages déchiffrés du serveur """
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                decrypted_message = vigenere_decrypt(message, CIPHER_KEY)
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
    root.protocol("WM_DELETE_WINDOW", client.close_client)  # Ferme la connexion proprement
    root.mainloop()
