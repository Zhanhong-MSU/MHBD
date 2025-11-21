#!/usr/bin/env python3
"""
Download complete 20 Newsgroups dataset (approximately 20,000 articles)
and save to dataset/newsgroups_full/ folder
"""

import os
import re
from sklearn.datasets import fetch_20newsgroups

def clean_filename(text, max_length=100):
    """Create a valid filename from text"""
    # Remove special characters
    filename = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces with underscores
    filename = re.sub(r'[-\s]+', '_', filename)
    # Truncate if too long
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename.strip('_')

def download_and_save_newsgroups():
    """Download all 20 Newsgroups data and save as individual text files"""
    
    print("Downloading 20 Newsgroups dataset...")
    print("This may take a few minutes on first download.\n")
    
    # Fetch both train and test sets to get all ~20,000 documents
    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
    newsgroups_test = fetch_20newsgroups(subset='test', remove=('headers', 'footers', 'quotes'))
    
    # Combine both datasets
    all_data = list(newsgroups_train.data) + list(newsgroups_test.data)
    all_targets = list(newsgroups_train.target) + list(newsgroups_test.target)
    
    # Category names
    categories = newsgroups_train.target_names
    
    print(f"Downloaded {len(all_data)} documents from {len(categories)} categories")
    print(f"\nCategories: {', '.join(categories)}\n")
    
    # Create output directory
    output_dir = "dataset/newsgroups_full"
    os.makedirs(output_dir, exist_ok=True)
    
    # Statistics
    category_counts = {}
    
    # Save each document
    for idx, (text, target) in enumerate(zip(all_data, all_targets), 1):
        category = categories[target]
        
        # Track category counts
        category_counts[category] = category_counts.get(category, 0) + 1
        
        # Clean the text
        text = text.strip()
        if not text or len(text) < 50:  # Skip very short documents
            continue
        
        # Create filename: doc_{number}_{category}.txt
        category_clean = category.replace('.', '_')
        filename = f"doc_{idx:05d}_{category_clean}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Save document
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Progress indicator
        if idx % 1000 == 0:
            print(f"Processed {idx} documents...")
    
    print(f"\n✓ Successfully saved {len(all_data)} documents to {output_dir}/")
    print("\nDocuments per category:")
    for category in sorted(category_counts.keys()):
        print(f"  {category}: {category_counts[category]} documents")
    
    return len(all_data), category_counts

if __name__ == "__main__":
    try:
        total, counts = download_and_save_newsgroups()
        print(f"\n✓ Download complete! Total documents: {total}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
