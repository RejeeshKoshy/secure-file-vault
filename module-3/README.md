# File Risk Checker

## Overview

A lightweight Python module to assess the riskiness of files based on:

* File extension validation against an allowed list
* MIME type verification using actual file content detection (via `python-magic`)
* Entropy analysis to detect potentially obfuscated or encrypted files

Useful for pre-upload validation in file storage or security applications.

---

## Features

* Validates file extensions against a whitelist
* Detects MIME type mismatches by inspecting file content
* Calculates Shannon entropy of file data to flag high-entropy files
* Provides detailed issue reports to help identify risky files

---

## Requirements

* Python 3.7+
* `python-magic` package (and system `libmagic`) for MIME detection

---

## Installation

1. Create and activate a Python virtual environment (optional but recommended)
2. Install dependencies:

   ```
   pip install python-magic
   ```
3. On Linux, install `libmagic` system library:

   ```
   sudo apt install libmagic1
   ```

---

## Usage

Run the checker against any file from the command line:

```
python3 main.py path/to/file
```

The script will output whether the file appears safe or list detected issues.

---

## Module API

* `is_file_suspicious(file_path: str, data: bytes) -> list[str]`
  Returns a list of detected issues or empty if the file is safe.

---

## Extending and Integrating

* Can be integrated into FastAPI or other APIs for real-time file validation
* Suitable for batch file scanning or pre-upload checks
* Easily extensible with custom checks or updated whitelist

---



