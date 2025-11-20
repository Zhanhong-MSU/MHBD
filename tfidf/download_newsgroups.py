#!/usr/bin/env python3
"""
Download 20 Newsgroups dataset for TF-IDF testing
"""
from sklearn.datasets import fetch_20newsgroups
import os

def download_newsgroups():
    """Download and save 20 Newsgroups dataset"""
    print("📥 Downloading 20 Newsgroups dataset...")
    
    # Create documents directory
    docs_dir = "documents"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print(f"✅ Created directory: {docs_dir}")
    
    # Download dataset (subset for faster download)
    categories = ['comp.graphics', 'sci.med', 'rec.sport.baseball', 
                  'talk.politics.misc', 'alt.atheism']
    
    print(f"📚 Fetching categories: {', '.join(categories)}")
    newsgroups = fetch_20newsgroups(subset='train', 
                                    categories=categories,
                                    remove=('headers', 'footers', 'quotes'))
    
    print(f"✅ Downloaded {len(newsgroups.data)} documents")
    
    # Save documents to files
    print("💾 Saving documents to files...")
    for i, (text, category_id) in enumerate(zip(newsgroups.data, newsgroups.target)):
        category_name = newsgroups.target_names[category_id]
        # Clean category name for filename
        safe_category = category_name.replace('.', '_')
        filename = f"{safe_category}_{i:04d}.txt"
        filepath = os.path.join(docs_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        if (i + 1) % 100 == 0:
            print(f"  Saved {i + 1}/{len(newsgroups.data)} documents...")
    
    print(f"🎉 Successfully saved {len(newsgroups.data)} documents to '{docs_dir}/' directory")
    
    # Create a summary file
    summary_path = os.path.join(docs_dir, "dataset_info.txt")
    with open(summary_path, 'w') as f:
        f.write("20 Newsgroups Dataset Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total documents: {len(newsgroups.data)}\n")
        f.write(f"Categories: {len(categories)}\n\n")
        f.write("Category breakdown:\n")
        for cat_id, cat_name in enumerate(newsgroups.target_names):
            count = sum(1 for t in newsgroups.target if t == cat_id)
            f.write(f"  - {cat_name}: {count} documents\n")
    
    print(f"📄 Dataset summary saved to '{summary_path}'")
    
    return len(newsgroups.data)

if __name__ == "__main__":
    try:
        count = download_newsgroups()
        print(f"\n✨ Ready to test TF-IDF with {count} documents!")
        print("📝 Next steps:")
        print("   1. Create input file: python3 create_tfidf_input.py")
        print("   2. Run TF-IDF: python3 tfidf.py --query 'your search terms' --input-dir '.' newsgroups_input.txt")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure to install scikit-learn: pip install scikit-learn")