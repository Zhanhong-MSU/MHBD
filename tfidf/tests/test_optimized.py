#!/usr/bin/env python3
"""
Optimized TF-IDF testing for large datasets
Pre-computes all TF-IDF values to avoid recalculation on each query
"""

import os
import sys
import time
import re
import math
from collections import Counter

def clean_text(text):
    """Clean and tokenize text"""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = text.split()
    # Remove very short words
    words = [w for w in words if len(w) > 2]
    return words

def calculate_tf(words):
    """Calculate Term Frequency"""
    total = len(words)
    if total == 0:
        return {}
    
    word_count = Counter(words)
    tf = {word: count / total for word, count in word_count.items()}
    return tf

def calculate_idf(doc_words_list):
    """Calculate Inverse Document Frequency"""
    num_docs = len(doc_words_list)
    
    # Count documents containing each word
    word_doc_count = Counter()
    for words in doc_words_list:
        unique_words = set(words)
        word_doc_count.update(unique_words)
    
    # Calculate IDF
    idf = {}
    for word, count in word_doc_count.items():
        idf[word] = math.log(num_docs / count)
    
    return idf

def precompute_tfidf(documents, doc_names):
    """Pre-compute TF-IDF for all documents"""
    print("Pre-computing TF-IDF scores...")
    start_time = time.time()
    
    # Clean all documents
    doc_words_list = [clean_text(doc) for doc in documents]
    
    # Calculate IDF
    idf = calculate_idf(doc_words_list)
    
    # Calculate TF-IDF for each document
    doc_tfidf = []
    for i, words in enumerate(doc_words_list):
        tf = calculate_tf(words)
        
        # Calculate TF-IDF for each word
        tfidf = {}
        for word, tf_val in tf.items():
            idf_val = idf.get(word, 0)
            tfidf[word] = tf_val * idf_val
        
        doc_tfidf.append({
            'name': doc_names[i],
            'tfidf': tfidf,
            'words': set(words)  # For fast lookup
        })
    
    elapsed = time.time() - start_time
    print(f"✓ Pre-computation completed in {elapsed:.2f} seconds")
    print(f"  Processed {len(documents):,} documents")
    print(f"  Vocabulary size: {len(idf):,} unique words\n")
    
    return doc_tfidf, idf

def search_optimized(query, doc_tfidf):
    """Fast search using pre-computed TF-IDF"""
    query_words = clean_text(query)
    
    results = []
    for doc_data in doc_tfidf:
        score = 0
        matching_words = 0
        
        for word in query_words:
            if word in doc_data['tfidf']:
                score += doc_data['tfidf'][word]
                matching_words += 1
        
        if len(query_words) > 0:
            score /= len(query_words)
        
        results.append((doc_data['name'], score, matching_words))
    
    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def run_optimized_test(doc_folder, queries, dataset_name):
    """Run optimized TF-IDF test"""
    print("\n" + "="*80)
    print(f" Testing Dataset: {dataset_name}")
    print("="*80)
    print(f"Document folder: {doc_folder}")
    print(f"Number of queries: {len(queries)}\n")
    
    # Check folder
    if not os.path.exists(doc_folder):
        print(f"✗ Error: Folder not found!")
        return None
    
    # Load documents
    print("Loading documents...")
    load_start = time.time()
    
    doc_files = sorted([f for f in os.listdir(doc_folder) if f.endswith('.txt')])
    documents = []
    doc_names = []
    total_words = 0
    
    for doc_file in doc_files[:]:  # Process all documents
        doc_path = os.path.join(doc_folder, doc_file)
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(content)
                doc_names.append(doc_file)
                total_words += len(content.split())
        except Exception as e:
            print(f"Warning: {doc_file}: {e}")
    
    load_time = time.time() - load_start
    print(f"✓ Loaded {len(documents):,} documents in {load_time:.2f} seconds")
    print(f"  Total words: {total_words:,}")
    print(f"  Average: {total_words // len(documents):,} words/doc\n")
    
    # Pre-compute TF-IDF
    doc_tfidf, idf = precompute_tfidf(documents, doc_names)
    precomp_time = time.time() - load_start - load_time
    
    # Run queries
    print(f"Running {len(queries)} queries...")
    print("-" * 80)
    
    query_times = []
    query_results = []
    
    for i, query in enumerate(queries, 1):
        query_start = time.time()
        results = search_optimized(query, doc_tfidf)
        query_time = time.time() - query_start
        query_times.append(query_time)
        
        if results:
            best_doc, best_score, matching = results[0]
            relevant_docs = len([r for r in results if r[1] > 0])
            
            query_results.append({
                'query': query,
                'best_doc': best_doc,
                'score': best_score,
                'time': query_time
            })
            
            print(f"Query {i}: {query}")
            print(f"  Best: {best_doc[:50]}")
            print(f"  Score: {best_score:.6f} | Time: {query_time:.4f}s | Relevant: {relevant_docs:,}")
        else:
            print(f"Query {i}: {query} - No results")
        print()
    
    # Summary
    total_time = time.time() - load_start
    avg_query_time = sum(query_times) / len(query_times) if query_times else 0
    
    print("="*80)
    print(f" Performance Summary - {dataset_name}")
    print("="*80)
    print(f"Documents:              {len(documents):,}")
    print(f"Total words:            {total_words:,}")
    print(f"Vocabulary size:        {len(idf):,}")
    print(f"Loading time:           {load_time:.2f}s")
    print(f"TF-IDF pre-compute:     {precomp_time:.2f}s")
    print(f"Total processing:       {total_time:.2f}s")
    print(f"Average query time:     {avg_query_time:.4f}s")
    print(f"Queries per second:     {len(queries)/sum(query_times):.2f}")
    print("="*80)
    
    return {
        'dataset': dataset_name,
        'num_docs': len(documents),
        'total_words': total_words,
        'vocab_size': len(idf),
        'load_time': load_time,
        'precomp_time': precomp_time,
        'total_time': total_time,
        'avg_query_time': avg_query_time,
        'query_results': query_results
    }

def print_comparison(results_list):
    """Print comparison between datasets"""
    if len(results_list) < 2:
        return
    
    print("\n" + "="*80)
    print(" Dataset Comparison (Optimized)")
    print("="*80)
    print(f"{'Metric':<30} {'Sample (10)':<20} {'Full (17,901)':<20} {'Ratio':<15}")
    print("-"*80)
    
    r1, r2 = results_list[0], results_list[1]
    
    metrics = [
        ('Documents', 'num_docs', ',', 'd'),
        ('Total Words', 'total_words', ',', 'd'),
        ('Vocabulary', 'vocab_size', ',', 'd'),
        ('Load Time', 'load_time', '.2f', 's'),
        ('TF-IDF Precompute', 'precomp_time', '.2f', 's'),
        ('Avg Query Time', 'avg_query_time', '.4f', 's'),
    ]
    
    for label, key, fmt, unit in metrics:
        v1 = r1[key]
        v2 = r2[key]
        
        if fmt == ',':
            s1 = f"{v1:,}"
            s2 = f"{v2:,}"
            ratio = f"{v2/v1:.1f}x" if v1 > 0 else "N/A"
        else:
            s1 = f"{v1:{fmt}}{unit}"
            s2 = f"{v2:{fmt}}{unit}"
            ratio = f"{v2/v1:.1f}x" if v1 > 0 else "N/A"
        
        print(f"{label:<30} {s1:<20} {s2:<20} {ratio:<15}")
    
    print("="*80)

def main():
    queries = [
        "computer graphics image rendering",
        "medical health disease treatment",
        "politics government election vote",
        "space nasa rocket satellite",
        "baseball game team player",
        "religion god belief christian",
        "car automobile vehicle engine",
        "encryption security cryptography"
    ]
    
    results = []
    
    # Test small dataset
    sample_folder = "dataset/newsgroups_sample"
    if os.path.exists(sample_folder):
        r1 = run_optimized_test(sample_folder, queries, "Newsgroups Sample")
        if r1:
            results.append(r1)
    
    # Test full dataset
    full_folder = "dataset/newsgroups_full"
    if os.path.exists(full_folder):
        r2 = run_optimized_test(full_folder, queries, "Newsgroups Full")
        if r2:
            results.append(r2)
    
    # Comparison
    if len(results) >= 2:
        print_comparison(results)
    
    print("\n✓ Testing complete!")

if __name__ == "__main__":
    main()
