# module-4/evaluate_model.py

import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

# Load dataset
df = pd.read_csv("data/dataset.csv")

# Load encoders
le_ext = joblib.load("model/label_encoder_ext.pkl")
le_mime = joblib.load("model/label_encoder_mime.pkl")

# Encode categorical features
df["ext_enc"] = df["ext"].apply(lambda x: le_ext.transform([x])[0] if x in le_ext.classes_ else -1)
df["mime_enc"] = df["mime"].apply(lambda x: le_mime.transform([x])[0] if x in le_mime.classes_ else -1)

# Prepare data
X = df[["size", "entropy", "ext_enc", "mime_enc"]]
y = df["label"]

# Load trained model
model = joblib.load("model/file_risk_model.pkl")

# Predict
y_pred = model.predict(X)
y_prob = model.predict_proba(X)[:, 1]

# === Confusion Matrix ===
cm = confusion_matrix(y, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Safe", "Risky"], yticklabels=["Safe", "Risky"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.savefig("plots/confusion_matrix.png")
plt.close()

# === ROC Curve ===
fpr, tpr, _ = roc_curve(y, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 4))
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("plots/roc_curve.png")
plt.close()

# === Classification Report (Printed) ===
print("\n📋 Classification Report:")
print(classification_report(y, y_pred, target_names=["Safe", "Risky"]))
print("✅ Saved: confusion_matrix.png, roc_curve.png to /plots/")
