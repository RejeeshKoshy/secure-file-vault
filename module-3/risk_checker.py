# risk_checker.py

import mimetypes
import math
import magic

# Define allowed safe file extensions
SAFE_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv'}

def check_extension(filename: str) -> bool:
    """Check if file extension is in the safe list."""
    ext = '.' + filename.rsplit('.', 1)[-1].lower()
    return ext in SAFE_EXTENSIONS

def check_mime(file_path: str, expected_mime: str) -> bool:
    """Compare expected MIME (from extension) with detected MIME (from content)."""
    detected_mime = magic.from_file(file_path, mime=True)
    return detected_mime == expected_mime

def calculate_entropy(data: bytes) -> float:
    """Estimate Shannon entropy of file data."""
    if not data:
        return 0.0
    freq = [0] * 256
    for byte in data:
        freq[byte] += 1
    entropy = -sum(
        (p := f / len(data)) * math.log2(p)
        for f in freq if f > 0
    )
    return entropy

def is_file_suspicious(file_path: str, data: bytes) -> list[str]:
    """Run all checks and return a list of detected issues."""
    issues = []

    filename = file_path.rsplit('/', 1)[-1]
    ext_check = check_extension(filename)

    expected_mime, _ = mimetypes.guess_type(filename)
    expected_mime = expected_mime or "application/octet-stream"

    if not ext_check:
        issues.append("Unrecognized or dangerous file extension.")

    if not check_mime(file_path, expected_mime):
        issues.append("MIME type mismatch.")

    entropy = calculate_entropy(data)
    if entropy > 7.5:
        issues.append(f"High entropy ({entropy:.2f}) suggests possible obfuscation.")

    return issues
