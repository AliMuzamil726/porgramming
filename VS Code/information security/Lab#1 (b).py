# -------- PLAYFAIR CIPHER --------

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J is merged with I

# Step 1: Generate Key Matrix
def generate_key_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []

    # Add key letters without duplicates
    for char in key:
        if char not in matrix and char in ALPHABET:
            matrix.append(char)

    # Add remaining alphabet letters
    for char in ALPHABET:
        if char not in matrix:
            matrix.append(char)

    # Convert into 5x5 matrix
    return [matrix[i:i+5] for i in range(0, 25, 5)]


# Step 2 & 3: Prepare plaintext
def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = "".join([c for c in text if c in ALPHABET])

    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = ""

        if i + 1 < len(text):
            b = text[i+1]
        else:
            b = "X"

        if a == b:
            prepared += a + "X"
            i += 1
        else:
            prepared += a + b
            i += 2

    if len(prepared) % 2 != 0:
        prepared += "X"

    return prepared


# Helper: Find position in matrix
def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col


# Step 5: Encrypt
def encrypt(plain_text, matrix):
    cipher_text = ""

    for i in range(0, len(plain_text), 2):
        a, b = plain_text[i], plain_text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        # Same row
        if row1 == row2:
            cipher_text += matrix[row1][(col1 + 1) % 5]
            cipher_text += matrix[row2][(col2 + 1) % 5]

        # Same column
        elif col1 == col2:
            cipher_text += matrix[(row1 + 1) % 5][col1]
            cipher_text += matrix[(row2 + 1) % 5][col2]

        # Rectangle rule
        else:
            cipher_text += matrix[row1][col2]
            cipher_text += matrix[row2][col1]

    return cipher_text


# Step 6: Decrypt
def decrypt(cipher_text, matrix):
    plain_text = ""

    for i in range(0, len(cipher_text), 2):
        a, b = cipher_text[i], cipher_text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        # Same row
        if row1 == row2:
            plain_text += matrix[row1][(col1 - 1) % 5]
            plain_text += matrix[row2][(col2 - 1) % 5]

        # Same column
        elif col1 == col2:
            plain_text += matrix[(row1 - 1) % 5][col1]
            plain_text += matrix[(row2 - 1) % 5][col2]

        # Rectangle rule
        else:
            plain_text += matrix[row1][col2]
            plain_text += matrix[row2][col1]

    return plain_text


# -------- MAIN PROGRAM --------
key = input("Enter key: ")
matrix = generate_key_matrix(key)

print("\nKey Matrix:")
for row in matrix:
    print(row)

plain_text = input("\nEnter plain text: ")
prepared_text = prepare_text(plain_text)

print("Prepared Text:", prepared_text)

cipher = encrypt(prepared_text, matrix)
print("Encrypted Text:", cipher)

decrypted = decrypt(cipher, matrix)
print("Decrypted Text:", decrypted)