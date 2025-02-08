import streamlit as st
import cv2
import numpy as np
import hashlib

# Function to hash the password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()[:16]  # 16-char hash

# Function to embed message and password into image
def encode_message(image, message, password):
    password_hash = hash_password(password)
    secret_data = password_hash + "þ" + message  # Include hashed password in the message
    binary_msg = ''.join(format(ord(i), '08b') for i in secret_data)
    binary_msg += '1111111111111110'  # End-of-message delimiter

    data_index = 0
    img = image.copy()
    for row in img:
        for pixel in row:
            for i in range(3):  # Loop through R, G, B
                if data_index < len(binary_msg):
                    pixel[i] = (pixel[i] & 254) | int(binary_msg[data_index])  # Ensure within 0-255 range
                    data_index += 1
                else:
                    return img
    return img

# Function to extract and verify password before showing message
def decode_message(image, password):
    binary_msg = ""
    for row in image:
        for pixel in row:
            for i in range(3):
                binary_msg += str(pixel[i] & 1)

    # Convert binary to text
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    extracted_data = "".join(chr(int(c, 2)) for c in chars)

    # Stop at the end-of-message delimiter
    extracted_data = extracted_data.split("þ")[0] if "þ" in extracted_data else ""

    # Extract stored password hash and message
    stored_password_hash = extracted_data[:16]
    hidden_message = extracted_data[17:]  # Remove the password part

    # Verify password
    if stored_password_hash == hash_password(password):
        return hidden_message
    else:
        return "⚠️ Incorrect Password! Image contains no visible message."

# Streamlit UI
st.title("🛡️ Secure Image Steganography App")

menu = st.sidebar.radio("Select an option:", ["Encrypt Message", "Decrypt Message"])

if menu == "Encrypt Message":
    st.header("🔐 Encrypt Message into Image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])
    message = st.text_area("Enter Secret Message")
    password = st.text_input("Set Encryption Password", type="password")

    if uploaded_file and message and password:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Encrypt and save
        encrypted_img = encode_message(image, message, password)
        cv2.imwrite("encrypted_image.png", encrypted_img)
        
        st.image(encrypted_img, caption="Encrypted Image (Appears Normal)", channels="BGR")
        st.download_button("Download Encrypted Image", open("encrypted_image.png", "rb").read(), "encrypted_image.png", "image/png")

elif menu == "Decrypt Message":
    st.header("🔓 Decrypt Message from Image")
    encrypted_file = st.file_uploader("Upload an encrypted image", type=["png", "jpg"])
    password = st.text_input("Enter Decryption Password", type="password")
    
    if encrypted_file and password:
        file_bytes = np.asarray(bytearray(encrypted_file.read()), dtype=np.uint8)
        encrypted_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Decrypt message
        hidden_msg = decode_message(encrypted_img, password)
        st.success(f"Decrypted Message: {hidden_msg}")
