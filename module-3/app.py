import streamlit as st
from risk_checker import is_file_suspicious

def main():
    st.title("🛡️ File Risk Checker")
    st.write("""
    This tool helps you quickly scan files to check if they might be risky before uploading or sharing.
    
    It performs checks including:
    - File extension validation (only common safe types allowed)
    - MIME type verification (checks actual file content)
    - Entropy analysis (detects files that may be encrypted or obfuscated)
    
    Upload a file below to see if it passes these security checks.
    """)

    uploaded_file = st.file_uploader("Choose a file to scan", type=None)

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        temp_path = f"temp_{uploaded_file.name}"

        with open(temp_path, "wb") as f:
            f.write(file_bytes)

        issues = is_file_suspicious(temp_path, file_bytes)

        st.markdown(f"### File info:")
        st.write(f"- **Name:** {uploaded_file.name}")
        st.write(f"- **Size:** {uploaded_file.size} bytes")

        if issues:
            st.error("⚠️ The file has the following issues:")
            for issue in issues:
                st.write(f"- {issue}")
            st.warning("Please be cautious uploading this file. It may be unsafe.")
        else:
            st.success("✅ This file appears safe based on our checks.")

        import os
        os.remove(temp_path)

if __name__ == "__main__":
    main()
