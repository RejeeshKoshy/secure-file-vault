import streamlit as st
import os
import magic
import joblib
import math
import pandas as pd

# === Load model and encoders ===
model = joblib.load("model/file_risk_model.pkl")
le_ext = joblib.load("model/label_encoder_ext.pkl")
le_mime = joblib.load("model/label_encoder_mime.pkl")

# === Feature extraction ===
def calculate_entropy(data):
    if not data:
        return 0
    freq = [0] * 256
    for byte in data:
        freq[byte] += 1
    entropy = -sum((f / len(data)) * math.log2(f / len(data)) for f in freq if f > 0)
    return round(entropy, 2)

def extract_features(uploaded_file):
    data = uploaded_file.read()
    size = len(data)
    entropy = calculate_entropy(data)
    ext = os.path.splitext(uploaded_file.name)[-1].lower().lstrip(".")
    
    with open("temp_file", "wb") as f:
        f.write(data)
    mime = magic.Magic(mime=True).from_file("temp_file")
    os.remove("temp_file")

    return size, entropy, ext, mime

# === Prediction ===
def predict(size, entropy, ext, mime):
    try:
        ext_enc = le_ext.transform([ext])[0]
    except:
        ext_enc = -1

    try:
        mime_enc = le_mime.transform([mime])[0]
    except:
        mime_enc = -1

    features = [[size, entropy, ext_enc, mime_enc]]
    prediction = model.predict(features)[0]
    return prediction

# === Streamlit UI ===
st.set_page_config(page_title="ML File Risk Checker", layout="centered")

st.title("🧠 ML-Based File Risk Checker")
st.markdown("Upload any file to check whether it's **safe or risky** based on a trained ML model.")

uploaded_file = st.file_uploader("Choose a file", type=None)

if uploaded_file is not None:
    size, entropy, ext, mime = extract_features(uploaded_file)
    prediction = predict(size, entropy, ext, mime)

    st.subheader("📋 File Details")
    st.write(pd.DataFrame({
        "Feature": ["Name", "Size (bytes)", "Entropy", "Extension", "MIME Type"],
        "Value": [uploaded_file.name, size, entropy, ext, mime]
    }))

    st.subheader("🛡️ ML Prediction")
    if prediction == 1:
        st.error("⚠️ This file is **RISKY**!")
    else:
        st.success("✅ This file is likely **SAFE**.")

    st.caption("Model trained on synthetic features — do not use in production.")

