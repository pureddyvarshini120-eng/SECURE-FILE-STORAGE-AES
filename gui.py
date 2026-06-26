import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
from cryptography.fernet import Fernet

# Load key
with open("secret.key", "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

def encrypt_file():
    filepath = filedialog.askopenfilename(title="Select file to encrypt")
    if not filepath:
        return
    with open(filepath, "rb") as f:
        data = f.read()
    original_hash = hashlib.sha256(data).hexdigest()
    encrypted_data = fernet.encrypt(data)
    enc_path = filepath + ".enc"
    with open(enc_path, "wb") as f:
        f.write(encrypted_data)
    hash_path = filepath + ".hash"
    with open(hash_path, "w") as f:
        f.write(original_hash)
    messagebox.showinfo("Success", f"Encrypted!\nSaved as: {enc_path}")

def decrypt_file():
    filepath = filedialog.askopenfilename(title="Select .enc file to decrypt")
    if not filepath:
        return
    with open(filepath, "rb") as f:
        encrypted_data = f.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception:
        messagebox.showerror("Error", "Decryption failed! File may be corrupted or tampered.")
        return
    dec_path = filepath.replace(".enc", "_decrypted")
    with open(dec_path, "wb") as f:
        f.write(decrypted_data)

    # Integrity check
    original_filename = filepath.replace(".enc", "")
    hash_path = original_filename + ".hash"
    try:
        with open(hash_path, "r") as f:
            original_hash = f.read().strip()
        new_hash = hashlib.sha256(decrypted_data).hexdigest()
        if new_hash == original_hash:
            integrity_msg = "Integrity check PASSED."
        else:
            integrity_msg = "Integrity check FAILED! File tampered."
    except FileNotFoundError:
        integrity_msg = "No hash file found."

    messagebox.showinfo("Success", f"Decrypted!\nSaved as: {dec_path}\n{integrity_msg}")

# GUI Setup
root = tk.Tk()
root.title("Secure File Storage System (AES)")
root.geometry("400x250")

title = tk.Label(root, text="🔐 Secure File Storage", font=("Arial", 16, "bold"))
title.pack(pady=20)

encrypt_btn = tk.Button(root, text="Encrypt File", font=("Arial", 12), width=20, command=encrypt_file)
encrypt_btn.pack(pady=10)

decrypt_btn = tk.Button(root, text="Decrypt File", font=("Arial", 12), width=20, command=decrypt_file)
decrypt_btn.pack(pady=10)

root.mainloop()