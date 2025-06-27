
import zipfile
import os
from datetime import datetime

def create_project_zip():
    # Get current timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"project_export_{timestamp}.zip"
    
    # Files to include in the zip
    files_to_zip = [
        'main.py',
        'pyproject.toml',
        '.replit',
        '.gitignore'
    ]
    
    # Create the zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Added {file} to zip")
            else:
                print(f"Warning: {file} not found, skipping")
    
    print(f"Project exported to: {zip_filename}")
    print(f"Zip file size: {os.path.getsize(zip_filename)} bytes")

if __name__ == "__main__":
    create_project_zip()
