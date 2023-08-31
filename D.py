import os
import winreg
from cryptography.fernet import Fernet

# Define the path to the folder
folder_path = r"C:\Users\K\Downloads\localRoot"

# Load the encryption key from the file
with open("encryption_key.key", "rb") as file:
    key = file.read()

# Create a Fernet cipher using the loaded key
cipher = Fernet(key)

# Function to decrypt a file
def decrypt_file(file_path):
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    new_file_path = file_path[:-7]
    with open(new_file_path, "wb") as file:
        file.write(decrypted_data)
    os.remove(file_path)
    print("Decrypted:", new_file_path)

# Traverse the folder and decrypt files
modified_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".kiriti"):
            file_path = os.path.join(root, file)
            decrypt_file(file_path)
            modified_files.append(file_path)

print("\nDecryption complete.")
print("Modified files:")
for file_path in modified_files:
    print(file_path)

# Specify the registry hives and key paths
registry_entries = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "MyEntry"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "MyEntry"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "MyEntry"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "MyEntry"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies", "MyEntry"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Policies", "MyEntry"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", "MyEntry"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", "MyEntry")
]

# Function to delete a registry entry
def delete_registry_entry(hive, key_path, value_name):
    try:
        with winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, value_name)
        print("Deleted:", key_path, value_name)
    except FileNotFoundError:
        print("Registry entry not found:", key_path, value_name)

# Delete the registry entries
for hive, key_path, value_name in registry_entries:
    delete_registry_entry(hive, key_path, value_name)

print("Registry entries deleted successfully.")
