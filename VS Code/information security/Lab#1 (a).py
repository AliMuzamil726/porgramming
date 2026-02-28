# Step 1: Create and initialize ALPHABET string
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Step 2: Read input
plain_text = input("Enter plain text: ").upper()
key = int(input("Enter Caesar cipher key (0–25): "))

# ---------------- ENCRYPTION ----------------
cipher_text = ""

for char in plain_text:
    if char in ALPHABET:
        # i. Find numeric representation
        plainnumeric = ALPHABET.index(char)

        # ii. Encryption formula
        ciphernumeric = (plainnumeric + key) % 26

        # iii. Get cipher character
        cipher_char = ALPHABET[ciphernumeric]
        cipher_text += cipher_char
    else:
        # keep spaces or symbols unchanged
        cipher_text += char

print("\nEncrypted Text:", cipher_text)

# ---------------- DECRYPTION ----------------
decrypted_text = ""

for char in cipher_text:
    if char in ALPHABET:
        # i. Find numeric representation
        ciphernumeric = ALPHABET.index(char)

        # ii. Decryption formula
        plainnumeric = (ciphernumeric - key) % 26

        # iii. Get original character
        plain_char = ALPHABET[plainnumeric]
        decrypted_text += plain_char
    else:
        decrypted_text += char

print("Decrypted Text:", decrypted_text)