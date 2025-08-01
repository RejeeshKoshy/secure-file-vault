# module-4/generate_dataset.py

import os
import csv
from extract_features import extract_features

# You can update this list based on what you know
label_map = {
    'safe.txt': 0,
    'renamed_exe.pdf': 0,
    'script.sh': 1,
    'random.bin': 1
}

DATA_DIR = "../module-3/test_files"
OUTPUT_FILE = "data/dataset.csv"

def main():
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["size", "entropy", "ext", "mime", "label"])
        writer.writeheader()

        for filename in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, filename)

            with open(filepath, "rb") as f:
                byte_data = f.read()

            features = extract_features(filepath, byte_data)
            features["label"] = label_map.get(filename, -1)  # default to -1 if not labeled
            writer.writerow(features)

    print(f"✅ Dataset written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
