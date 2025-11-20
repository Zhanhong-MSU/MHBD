#!/usr/bin/env python3
"""
Create TF-IDF input file from 20 Newsgroups documents
"""
import os

def create_tfidf_input():
    """Create tab-separated input file for TF-IDF from documents directory"""
    docs_dir = "documents"
    output_file = "newsgroups_input.txt"
    
    if not os.path.exists(docs_dir):
        print(f"❌ Directory '{docs_dir}' not found!")
        print("💡 Run 'python3 download_newsgroups.py' first to download the dataset")
        return
    
    print(f"📂 Reading documents from '{docs_dir}'...")
    
    # Get all text files
    files = [f for f in os.listdir(docs_dir) if f.endswith('.txt') and f != 'dataset_info.txt']
    
    if not files:
        print(f"❌ No .txt files found in '{docs_dir}'")
        return
    
    print(f"📝 Processing {len(files)} documents...")
    
    # Create input file
    with open(output_file, 'w', encoding='utf-8') as out:
        for i, filename in enumerate(sorted(files)):
            filepath = os.path.join(docs_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    # Replace newlines and tabs to keep format clean
                    content = content.replace('\n', ' ').replace('\t', ' ')
                    # Write filename and content separated by tab
                    out.write(f"{filename}\t{content}\n")
                
                if (i + 1) % 100 == 0:
                    print(f"  Processed {i + 1}/{len(files)} documents...")
            except Exception as e:
                print(f"⚠️  Error reading {filename}: {e}")
    
    print(f"✅ Created '{output_file}' with {len(files)} documents")
    print(f"\n📊 File size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
    
    # Show sample queries
    print("\n🔍 Example queries to try:")
    print("   python3 tfidf.py --query 'computer graphics' --input-dir '.' newsgroups_input.txt")
    print("   python3 tfidf.py --query 'medical health' --input-dir '.' newsgroups_input.txt")
    print("   python3 tfidf.py --query 'baseball game' --input-dir '.' newsgroups_input.txt")
    print("   python3 tfidf.py --query 'politics government' --input-dir '.' newsgroups_input.txt")
    print("   python3 tfidf.py --query 'religion atheism' --input-dir '.' newsgroups_input.txt")

if __name__ == "__main__":
    create_tfidf_input()