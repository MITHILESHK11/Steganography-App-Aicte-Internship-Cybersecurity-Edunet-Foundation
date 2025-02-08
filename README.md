# 🛡️ Secure Image Steganography App

## 📌 Overview
This is a **password-protected image steganography app** built using **Streamlit** and **OpenCV**. It allows you to **hide secret messages inside images** and retrieve them only with the correct password.

## 🚀 Features
- **Encrypt Secret Messages** into images without visible changes.
- **Decrypt Messages Securely** using a password.
- **If the wrong password is entered, the image appears normal** (prevents detection).
- **Download Encrypted Images** after embedding messages.

## 🏗️ Technologies Used
- **Python** (Backend Logic)
- **Streamlit** (User Interface)
- **OpenCV** (Image Processing)
- **NumPy** (Efficient Data Handling)
- **Hashlib** (Password Hashing for Security)

## 📥 Installation Guide
### 🔹 1️⃣ Install Dependencies
```bash
pip install streamlit opencv-python numpy
```

### 🔹 2️⃣ Run the Application
```bash
streamlit run app.py
```

## 🛠️ Usage Guide
### **🔐 Encrypting a Message**
1. Open the app.
2. Select **Encrypt Message** from the sidebar.
3. Upload an image (`.jpg` or `.png`).
4. Enter a secret message.
5. Set an **encryption password**.
6. Click **Encrypt** to hide the message in the image.
7. Download the encrypted image.

### **🔓 Decrypting a Message**
1. Open the app.
2. Select **Decrypt Message** from the sidebar.
3. Upload the encrypted image.
4. Enter the **correct decryption password**.
5. Click **Decrypt** to reveal the hidden message.

## 🔍 How It Works
1. **Encoding Process:**
   - The message is converted into binary.
   - A **password hash** is added for authentication.
   - The binary data is hidden in the **least significant bit (LSB)** of the image.

2. **Decoding Process:**
   - Extracts binary data from the image.
   - Verifies the password before revealing the hidden message.
   - If the password is wrong, the image appears as a normal image.

## 🔐 Security Measures
- **Password Protection:** Messages can only be decrypted with the correct password.
- **Stealth Mode:** Without the correct password, the image looks normal.
- **End Marker:** Prevents over-reading of hidden data.

## 📜 License
This project is open-source and available under the **MIT License**.
---
Enjoy Secure Messaging! 🔒
