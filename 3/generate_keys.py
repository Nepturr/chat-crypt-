import rsa

# Générer la paire de clés RSA (2048 bits)
public_key, private_key = rsa.newkeys(2048)

# Sauvegarder la clé privée
with open("private_key.pem", "wb") as f:
    f.write(private_key.save_pkcs1())

# Sauvegarder la clé publique
with open("public_key.pem", "wb") as f:
    f.write(public_key.save_pkcs1())

print("✅ Clés RSA générées avec succès !")
