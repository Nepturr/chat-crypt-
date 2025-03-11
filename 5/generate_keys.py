import rsa
import os

# Vérifier si le dossier "5" existe, sinon le créer
key_dir = "keys"
if not os.path.exists(key_dir):
    os.makedirs(key_dir)

# Générer la paire de clés RSA (2048 bits)
public_key, private_key = rsa.newkeys(2048)

# Sauvegarder la clé privée
with open(os.path.join(key_dir, "private_key.pem"), "wb") as f:
    f.write(private_key.save_pkcs1())

# Sauvegarder la clé publique
with open(os.path.join(key_dir, "public_key.pem"), "wb") as f:
    f.write(public_key.save_pkcs1())

print(f"✅ Clés RSA générées avec succès dans {key_dir}/")
