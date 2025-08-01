# module-4/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
df = pd.read_csv("data/dataset.csv")

# Encode categorical features
le_ext = LabelEncoder()
le_mime = LabelEncoder()
df["ext_enc"] = le_ext.fit_transform(df["ext"])
df["mime_enc"] = le_mime.fit_transform(df["mime"])

# Features and labels
X = df[["size", "entropy", "ext_enc", "mime_enc"]]
y = df["label"]

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("✅ Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save model and encoders
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/file_risk_model.pkl")
joblib.dump(le_ext, "model/label_encoder_ext.pkl")
joblib.dump(le_mime, "model/label_encoder_mime.pkl")

print("\n✅ Model and encoders saved to 'model/' folder.")
