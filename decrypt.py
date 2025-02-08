import cv2
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16]  # 16-char hash

def decode_message(image, password):
    binary_msg = ""
    for row in image:
        for pixel in row:
            for i in range(3):
                binary_msg += str(pixel[i] & 1)

    # Stop at the end-of-message delimiter
    delimiter = '1111111111111110'
    end_index = binary_msg.find(delimiter)
    if end_index != -1:
        binary_msg = binary_msg[:end_index]

    # Convert binary to text
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    extracted_data = "".join(chr(int(c, 2)) for c in chars)

    # Extract stored password hash and message
    stored_password_hash = extracted_data[:16]  # Extract the first 16 characters (hash)
    hidden_message = extracted_data[17:] if len(extracted_data) > 17 else ""  # Extract the actual message

    # Verify password
    if stored_password_hash == hash_password(password):
        return hidden_message
    else:
        return "⚠️ Incorrect Password! Image contains no visible message."
