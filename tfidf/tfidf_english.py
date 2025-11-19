#!/usr/bin/env python3
"""
TF-IDF Implementation - Standalone Version
For assignment submission - works on any VPS with Python 3

Requirements: Only Python 3 standard library (no external dependencies)
Usage: python3 tfidf_english.py
"""

import re
import math
import os
from collections import defaultdict, Counter

def clean_text(text):
    """Clean and tokenize text"""
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def calculate_tf(word_list):
    """Calculate term frequency"""
    word_count = len(word_list)
    tf_dict = {}
    counter = Counter(word_list)
    
    for word, count in counter.items():
        tf_dict[word] = count / word_count
    
    return tf_dict

def calculate_idf(documents):
    """Calculate inverse document frequency"""
    total_docs = len(documents)
    idf_dict = {}
    all_words = set(word for doc in documents for word in doc)
    
    for word in all_words:
        docs_containing_word = sum(1 for doc in documents if word in doc)
        idf_dict[word] = math.log(total_docs / docs_containing_word)
    
    return idf_dict

def search_documents(documents, query, doc_names):
    """Search documents using TF-IDF"""
    # Prepare documents
    doc_words = []
    for doc_content in documents:
        words = clean_text(doc_content)
        doc_words.append(words)
    
    # Calculate IDF
    idf = calculate_idf(doc_words)
    
    # Calculate TF-IDF for each document
    doc_scores = []
    query_words = clean_text(query)
    
    for i, words in enumerate(doc_words):
        tf = calculate_tf(words)
        
        # Calculate relevance score for query
        score = 0
        matching_words = []
        for word in query_words:
            tf_val = tf.get(word, 0)
            idf_val = idf.get(word, 0)
            tfidf_score = tf_val * idf_val
            score += tfidf_score
            
            if tf_val > 0:
                matching_words.append((word, tf_val, idf_val, tfidf_score))
        
        if len(query_words) > 0:
            score /= len(query_words)  # Average score
        
        doc_scores.append((doc_names[i], score, matching_words))
    
    # Sort by score (descending)
    doc_scores.sort(key=lambda x: x[1], reverse=True)
    return doc_scores

def main():
    # Read documents from documents directory
    documents = []
    doc_names = []
    documents_dir = 'documents'
    
    if not os.path.exists(documents_dir):
        print(f"Error: {documents_dir} directory not found")
        return
    
    # Read all text files in the documents directory
    for filename in sorted(os.listdir(documents_dir)):
        if filename.endswith('.txt'):
            filepath = os.path.join(documents_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:  # Only add non-empty files
                        doc_names.append(filename)
                        documents.append(content)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    if not documents:
        print("No documents found in the documents directory")
        return
    
    print("TF-IDF Algorithm Results")
    print("=" * 80)
    print()
    
    # Display document summary
    print(f"Input Documents ({len(documents)} files):")
    for i, (name, content) in enumerate(zip(doc_names, documents), 1):
        # Show first 100 characters of each document
        preview = content[:100] + "..." if len(content) > 100 else content
        print(f"{i}. {name}: {preview}")
    print()
    
    # Test queries relevant to the academic papers
    queries = [
        "machine learning healthcare",
        "deep learning natural language",
        "data science business analytics",
        "artificial intelligence ethics",
        "computer vision autonomous systems",
        "neural networks algorithms",
        "predictive analytics",
        "transformer models"
    ]
    
    for query in queries:
        print(f"Query: '{query}'")
        print("-" * 40)
        
        results = search_documents(documents, query, doc_names)
        
        for rank, (doc_name, score, matching_words) in enumerate(results, 1):
            print(f"{rank}. {doc_name} (Score: {score:.4f})")
            
            if matching_words:
                print("   Matching terms:")
                for word, tf_val, idf_val, tfidf in matching_words:
                    print(f"     '{word}': TF={tf_val:.4f}, IDF={idf_val:.4f}, TF-IDF={tfidf:.4f}")
            else:
                print("   (No matching terms found)")
        print()

if __name__ == "__main__":
    main()