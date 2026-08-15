import tkinter as tk
from tkinter import ttk, messagebox

# Caesar Cipher
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def caesar_bruteforce(text):
    results = ""
    for shift in range(26):
        results += f"Shift {shift}: {caesar_decrypt(text, shift)}\n"
    return results

# Vigenere Cipher
def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    j = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[j % len(key)]) - 97
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
            j += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    j = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[j % len(key)]) - 97
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base - shift) % 26 + base)
            j += 1
        else:
            result += char
    return result

# Rail Fence Cipher
def rail_fence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction

        if rail == 0 or rail == rails - 1:
            direction *= -1

    return ''.join(''.join(row) for row in fence)

def rail_fence_decrypt(cipher, rails):
    fence = [[] for _ in range(rails)]
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    rail_pattern = [pattern[i % len(pattern)] for i in range(len(cipher))]

    index = 0
    for r in range(rails):
        for i in range(len(cipher)):
            if rail_pattern[i] == r:
                fence[r].append(cipher[index])
                index += 1

    result = ""
    pointers = [0] * rails

    for r in rail_pattern:
        result += fence[r][pointers[r]]
        pointers[r] += 1

    return result

# Functions
def process():
    cipher = combo_cipher.get()
    mode = combo_mode.get()
    text = entry_text.get()
    key = entry_key.get()

    try:
        if cipher == "Caesar":
            shift = int(key)
            if mode == "Encrypt":
                result = caesar_encrypt(text, shift)
            elif mode == "Decrypt":
                result = caesar_decrypt(text, shift)
            else:
                result = caesar_bruteforce(text)

        elif cipher == "Vigenere":
            if mode == "Encrypt":
                result = vigenere_encrypt(text, key)
            else:
                result = vigenere_decrypt(text, key)

        elif cipher == "Rail Fence":
            rails = int(key)
            if mode == "Encrypt":
                result = rail_fence_encrypt(text, rails)
            else:
                result = rail_fence_decrypt(text, rails)

        output.delete("1.0", tk.END)
        output.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_fields():
    entry_text.delete(0, tk.END)
    entry_key.delete(0, tk.END)
    output.delete("1.0", tk.END)


def copy_result():
    result = output.get("1.0", tk.END)
    app.clipboard_clear()
    app.clipboard_append(result)
    messagebox.showinfo("Copied", "Result copied to clipboard ✅")


# UI
app = tk.Tk()
app.title("Cipher System 🔐")
app.geometry("520x550")
app.configure(bg="#1e1e1e")

title = tk.Label(app, text="Encryption System", fg="white", bg="#1e1e1e", font=("Arial", 16))
title.pack(pady=10)

combo_cipher = ttk.Combobox(app, values=["Caesar", "Vigenere", "Rail Fence"])
combo_cipher.set("Caesar")
combo_cipher.pack(pady=5)

combo_mode = ttk.Combobox(app, values=["Encrypt", "Decrypt", "Brute Force (Caesar only)"])
combo_mode.set("Encrypt")
combo_mode.pack(pady=5)

entry_text = tk.Entry(app, width=45)
entry_text.pack(pady=10)
entry_text.insert(0, "Enter text")

entry_key = tk.Entry(app, width=45)
entry_key.pack(pady=10)
entry_key.insert(0, "Enter key")

# Buttons Frame
frame_buttons = tk.Frame(app, bg="#1e1e1e")
frame_buttons.pack(pady=10)

btn_run = tk.Button(frame_buttons, text="Run", command=process, bg="#4CAF50", fg="white", width=10)
btn_run.grid(row=0, column=0, padx=5)

btn_clear = tk.Button(frame_buttons, text="Clear", command=clear_fields, bg="#f44336", fg="white", width=10)
btn_clear.grid(row=0, column=1, padx=5)

btn_copy = tk.Button(frame_buttons, text="Copy", command=copy_result, bg="#2196F3", fg="white", width=10)
btn_copy.grid(row=0, column=2, padx=5)

output = tk.Text(app, height=12, width=60)
output.pack(pady=10)

app.mainloop()