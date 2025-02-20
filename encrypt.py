import cv2
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16]  # 16-char hash

def encode_message(image, message, password):
    password_hash = hash_password(password)
    secret_data = password_hash + "þ" + message  # Include hashed password in the message
    binary_msg = ''.join(format(ord(i), '08b') for i in secret_data)
    binary_msg += '1111111111111110'  # End-of-message delimiter

    data_index = 0
    img = image.copy()
    for row in img:
        for pixel in row:
            for i in range(3): 
                if data_index < len(binary_msg):
                    pixel[i] = (pixel[i] & 254) | int(binary_msg[data_index])  
                    data_index += 1
                else:
                    return img
    return img
