#!/usr/bin/env python3
"""
TF-IDF Analysis Demonstration - Standalone Version
Academic Paper Document Collection Analysis
Works on any VPS with Python 3
"""

import os
import sys

def main():
    print("="*80)
    print("TF-IDF ALGORITHM DEMONSTRATION")
    print("Academic Paper Document Collection Analysis")
    print("="*80)
    print()
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return 1
    
    # Show document collection
    documents_dir = 'documents'
    if not os.path.exists(documents_dir):
        print(f"❌ Error: {documents_dir} directory not found")
        return 1
        
    print(f"📚 Document Collection ({documents_dir}/):")
    print("-" * 50)
    
    doc_count = 0
    total_words = 0
    
    try:
        for filename in sorted(os.listdir(documents_dir)):
            if filename.endswith('.txt'):
                filepath = os.path.join(documents_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    word_count = len(content.split())
                    total_words += word_count
                    doc_count += 1
                    
                    # Extract title (first line)
                    title = content.split('\n')[0]
                    print(f"{doc_count}. {filename}")
                    print(f"   Title: {title}")
                    print(f"   Size: {word_count:,} words, {len(content):,} characters")
                    print()
    except Exception as e:
        print(f"❌ Error reading documents: {e}")
        return 1
    
    if doc_count == 0:
        print("❌ No text documents found in documents/ directory")
        return 1
    
    print(f"✅ Total Collection: {doc_count} documents, {total_words:,} words")
    print()
    
    print("🔍 RUNNING TF-IDF ANALYSIS")
    print("="*80)
    
    # Import and run TF-IDF analysis directly
    try:
        # Import the main function from tfidf_english
        import importlib.util
        spec = importlib.util.spec_from_file_location("tfidf_english", "tfidf_english.py")
        tfidf_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tfidf_module)
        
        # Run the analysis
        tfidf_module.main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return 1
    
    print("="*80)
    print("✅ ANALYSIS COMPLETE")
    print("This demonstrates TF-IDF algorithm performance on academic papers")
    print("covering Machine Learning, Deep Learning, Data Science, AI Ethics,")
    print("and Computer Vision topics.")
    print("="*80)
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)