# extract_features.py

import os
import math
import mimetypes
from collections import Counter

def calculate_entropy(byte_data):
    if not byte_data:
        return 0
    byte_counts = Counter(byte_data)
    total = len(byte_data)
    entropy = -sum((count/total) * math.log2(count/total) for count in byte_counts.values())
    return entropy

def extract_features(filepath, byte_data):
    size = len(byte_data)
    entropy = calculate_entropy(byte_data)
    _, ext = os.path.splitext(filepath)
    mime_type = mimetypes.guess_type(filepath)[0] or "unknown"

    features = {
        "size": size,
        "entropy": entropy,
        "ext": ext.lower().replace('.', ''),
        "mime": mime_type.split('/')[-1] if '/' in mime_type else mime_type,
    }

    return features
