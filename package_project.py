"""
Packages clean project source code into a ZIP archive for submission.
"""

import os
import zipfile

def package_source():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, "deliverables", "Smart_Resume_Analyzer_Source_Code.zip")
    
    exclude_dirs = {"deliverables", "__pycache__", ".git", ".venv", "env"}
    exclude_exts = {".pyc", ".zip"}

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in exclude_exts or file.endswith(".db"):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                zipf.write(full_path, rel_path)

    print(f"Created clean source code package: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    package_source()
