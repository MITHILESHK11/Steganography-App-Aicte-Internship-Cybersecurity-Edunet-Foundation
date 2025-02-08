import streamlit as st
import cv2
import numpy as np
import os

# Function to embed message into image
def encode_message(image, message):
    binary_msg = ''.join(format(ord(i), '08b') for i in message)
    binary_msg += '1111111111111110'  # End-of-message delimiter

    data_index = 0
    img = image.copy()
    for row in img:
        for pixel in row:
            for i in range(3):  # Loop through R, G, B
                if data_index < len(binary_msg):
                    pixel[i] = pixel[i] & ~1 | int(binary_msg[data_index])
                    data_index += 1
                else:
                    return img
    return img

# Function to extract message from image
def decode_message(image):
    binary_msg = ""
    for row in image:
        for pixel in row:
            for i in range(3):
                binary_msg += str(pixel[i] & 1)

    # Convert binary to text
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
    message = "".join(chr(int(c, 2)) for c in chars)

    # Stop at the end-of-message delimiter
    return message.split("þ")[0]  # 'þ' is a special delimiter

# Streamlit UI
st.title("🛡️ Image Steganography App")

menu = st.sidebar.radio("Select an option:", ["Encrypt Message", "Decrypt Message"])

if menu == "Encrypt Message":
    st.header("🔐 Encrypt Message into Image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])
    message = st.text_area("Enter Secret Message")

    if uploaded_file and message:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Encrypt and save
        encrypted_img = encode_message(image, message)
        cv2.imwrite("encrypted_image.png", encrypted_img)
        
        st.image(encrypted_img, caption="Encrypted Image", channels="BGR")
        st.download_button("Download Encrypted Image", open("encrypted_image.png", "rb").read(), "encrypted_image.png", "image/png")

elif menu == "Decrypt Message":
    st.header("🔓 Decrypt Message from Image")
    encrypted_file = st.file_uploader("Upload an encrypted image", type=["png", "jpg"])
    
    if encrypted_file:
        file_bytes = np.asarray(bytearray(encrypted_file.read()), dtype=np.uint8)
        encrypted_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Decrypt message
        hidden_msg = decode_message(encrypted_img)
        st.success(f"Decrypted Message: {hidden_msg}")

