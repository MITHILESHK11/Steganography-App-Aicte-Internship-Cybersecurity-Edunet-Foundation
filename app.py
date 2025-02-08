import streamlit as st
import cv2
import numpy as np
from encrypt import encode_message
from decrypt import decode_message

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

