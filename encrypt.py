import hashlib
from cryptography.fernet import Fernet

# Load the key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# File to encrypt
filename = input("Enter the filename to encrypt (with extension): ")

with open(filename, "rb") as file:
    original_data = file.read()

# Calculate hash of original file (for integrity check later)
original_hash = hashlib.sha256(original_data).hexdigest()

# Encrypt the data
encrypted_data = fernet.encrypt(original_data)

# Save encrypted file
encrypted_filename = filename + ".enc"
with open(encrypted_filename, "wb") as enc_file:
    enc_file.write(encrypted_data)

# Save hash in a separate metadata file
hash_filename = filename + ".hash"
with open(hash_filename, "w") as hash_file:
    hash_file.write(original_hash)

print(f"File '{filename}' encrypted successfully as '{encrypted_filename}'")
print(f"Original file hash (SHA-256): {original_hash}")
print(f"Hash saved as '{hash_filename}' for integrity verification")