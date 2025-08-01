# module-4/predict_file.py

import os
import magic
import math
import joblib
import sys

# === Feature Extraction ===
def get_file_features(file_path):
    size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        data = f.read()
    entropy = calculate_entropy(data)
    ext = os.path.splitext(file_path)[-1].lower().lstrip(".")
    mime = magic.Magic(mime=True).from_file(file_path)
    return size, entropy, ext, mime

def calculate_entropy(data):
    if not data:
        return 0
    freq = [0] * 256
    for byte in data:
        freq[byte] += 1
    entropy = -sum((f / len(data)) * math.log2(f / len(data)) for f in freq if f > 0)
    return round(entropy, 2)

# === Load Model & Encoders ===
model = joblib.load("model/file_risk_model.pkl")
le_ext = joblib.load("model/label_encoder_ext.pkl")
le_mime = joblib.load("model/label_encoder_mime.pkl")

# === Predict ===
def predict_risk(file_path):
    size, entropy, ext, mime = get_file_features(file_path)

    try:
        ext_enc = le_ext.transform([ext])[0]
    except:
        ext_enc = -1  # unknown = -1

    try:
        mime_enc = le_mime.transform([mime])[0]
    except:
        mime_enc = -1  # unknown = -1

    features = [[size, entropy, ext_enc, mime_enc]]
    prediction = model.predict(features)[0]

    print(f"\n📂 File: {file_path}")
    print(f"🔍 Size: {size} bytes, Entropy: {entropy}, Ext: {ext}, MIME: {mime}")
    print("🛡️ Prediction:", "⚠️ Risky!" if prediction else "✅ Safe")

# === CLI usage ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 predict_file.py <file_path>")
        sys.exit(1)

    predict_risk(sys.argv[1])
