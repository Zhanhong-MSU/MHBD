#!/usr/bin/env python3
"""
Dataset Management Script for TF-IDF Project
Allows deleting the full dataset to save space and downloading/restoring it from the web.

Usage:
    python manage_dataset.py delete
    python manage_dataset.py download
"""

import os
import sys
import shutil
import tarfile
import urllib.request
import ssl

# Configuration
DATASET_URL = "http://qwone.com/~jason/20Newsgroups/20news-18828.tar.gz"
DATASET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset", "newsgroups_full")
TEMP_ARCHIVE = "20news-18828.tar.gz"

def delete_dataset():
    """Delete the newsgroups_full directory."""
    if os.path.exists(DATASET_DIR):
        print(f"🗑️  Deleting {DATASET_DIR}...")
        shutil.rmtree(DATASET_DIR)
        print("✅ Dataset deleted successfully.")
    else:
        print(f"⚠️  Directory {DATASET_DIR} does not exist.")

def download_dataset():
    """Download and reconstruct the dataset."""
    # Create directory if it doesn't exist
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        print(f"📂 Created directory {DATASET_DIR}")
    else:
        print(f"⚠️  Directory {DATASET_DIR} already exists. Merging/Overwriting...")

    # Download
    print(f"⬇️  Downloading dataset from {DATASET_URL}...")
    try:
        # Bypass SSL verification for older environments if needed, though standard should work
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(DATASET_URL, context=context) as response, open(TEMP_ARCHIVE, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("✅ Download complete.")
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return

    # Extract
    print("📦 Extracting archive...")
    try:
        with tarfile.open(TEMP_ARCHIVE, "r:gz") as tar:
            tar.extractall()
        print("✅ Extraction complete.")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        if os.path.exists(TEMP_ARCHIVE):
            os.remove(TEMP_ARCHIVE)
        return

    # Flatten and Rename
    print("🔄 Processing and flattening files...")
    extracted_root = "20news-18828"
    if not os.path.exists(extracted_root):
        print(f"❌ Error: Extracted directory '{extracted_root}' not found.")
        return

    count = 0
    for category in os.listdir(extracted_root):
        category_path = os.path.join(extracted_root, category)
        if os.path.isdir(category_path):
            # Normalize category name (comp.graphics -> comp_graphics)
            clean_category = category.replace('.', '_')
            
            for filename in os.listdir(category_path):
                file_path = os.path.join(category_path, filename)
                if os.path.isfile(file_path):
                    # Create new filename: doc_{id}_{category}.txt
                    # We use the original filename as ID
                    new_filename = f"doc_{filename}_{clean_category}.txt"
                    dest_path = os.path.join(DATASET_DIR, new_filename)
                    
                    shutil.move(file_path, dest_path)
                    count += 1
    
    print(f"✅ Processed {count} documents.")

    # Cleanup
    print("🧹 Cleaning up temporary files...")
    if os.path.exists(TEMP_ARCHIVE):
        os.remove(TEMP_ARCHIVE)
    if os.path.exists(extracted_root):
        shutil.rmtree(extracted_root)
    
    print("✨ Dataset restored successfully!")

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['delete', 'download']:
        print(__doc__)
        return

    command = sys.argv[1]
    if command == 'delete':
        delete_dataset()
    elif command == 'download':
        download_dataset()

if __name__ == "__main__":
    main()
