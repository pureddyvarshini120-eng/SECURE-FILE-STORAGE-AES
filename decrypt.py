import hashlib
from cryptography.fernet import Fernet

# Load the key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# File to decrypt
filename = input("Enter the encrypted filename (with .enc extension): ")

with open(filename, "rb") as file:
    encrypted_data = file.read()

try:
    decrypted_data = fernet.decrypt(encrypted_data)
except Exception:
    print("ERROR: Decryption failed! File may be corrupted, tampered, or wrong key used.")
    exit()

# Save decrypted file
decrypted_filename = filename.replace(".enc", "_decrypted")
with open(decrypted_filename, "wb") as dec_file:
    dec_file.write(decrypted_data)

print(f"File '{filename}' decrypted successfully as '{decrypted_filename}'")

# Verify integrity using saved hash
original_filename = filename.replace(".enc", "")
hash_filename = original_filename + ".hash"

try:
    with open(hash_filename, "r") as hash_file:
        original_hash = hash_file.read().strip()

    # Calculate hash of decrypted data
    new_hash = hashlib.sha256(decrypted_data).hexdigest()

    if new_hash == original_hash:
        print("Integrity check PASSED: File is unaltered.")
    else:
        print("Integrity check FAILED: File may have been tampered!")

except FileNotFoundError:
    print("No hash file found, skipping integrity check.")