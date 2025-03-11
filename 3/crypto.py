# crypto.py
import itertools

# Chiffrement César
def cesar_encrypt(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift if char.islower() else shift
            new_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift_amount) % 26) + ord('a' if char.islower() else 'A'))
            result += new_char
        else:
            result += char
    return result

def cesar_decrypt(text, shift=3):
    return cesar_encrypt(text, -shift)

# Chiffrement Vigenère
def vigenere_encrypt(text, key):
    key_cycle = itertools.cycle(key)
    result = ""

    for char in text:
        if char.isalpha():
            shift = ord(next(key_cycle).lower()) - ord('a')
            new_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26) + ord('a' if char.islower() else 'A'))
            result += new_char
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    key_cycle = itertools.cycle(key)
    result = ""

    for char in text:
        if char.isalpha():
            shift = ord(next(key_cycle).lower()) - ord('a')
            new_char = chr(((ord(char) - ord('a' if char.islower() else 'A') - shift) % 26) + ord('a' if char.islower() else 'A'))
            result += new_char
        else:
            result += char
    return result
