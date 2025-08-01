# main.py

from risk_checker import is_file_suspicious
import sys
import os

def load_file(path: str) -> bytes:
    """Read binary contents of a file."""
    with open(path, 'rb') as f:
        return f.read()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' does not exist or is not a file.")
        sys.exit(1)

    file_data = load_file(filepath)
    issues = is_file_suspicious(filepath, file_data)

    print("\n🧪 File Risk Check Result:")
    print(f"🗂️ File: {filepath}")

    if issues:
        print("⚠️  Suspicious file detected!")
        for issue in issues:
            print(" -", issue)
    else:
        print("✅ File appears safe.")

if __name__ == "__main__":
    main()
