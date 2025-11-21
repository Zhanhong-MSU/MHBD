#!/usr/bin/env python3
"""
Test TF-IDF on both newsgroups datasets:
1. Small sample (10 documents)
2. Full dataset (18,846 documents)
"""

import os
import sys
import time

def run_tfidf_analysis(doc_folder, queries, dataset_name):
    """Run TF-IDF analysis on a specific dataset"""
    print("\n" + "="*80)
    print(f" Testing Dataset: {dataset_name}")
    print("="*80)
    print(f"Document folder: {doc_folder}")
    print(f"Number of queries: {len(queries)}")
    
    # Import the TF-IDF module
    from run_analysis import search_documents, calculate_idf
    from collections import Counter
    
    # Check if folder exists
    if not os.path.exists(doc_folder):
        print(f"✗ Error: Folder '{doc_folder}' does not exist!")
        return
    
    # Get all documents
    doc_files = sorted([f for f in os.listdir(doc_folder) if f.endswith('.txt')])
    
    if not doc_files:
        print(f"✗ Error: No .txt files found in '{doc_folder}'!")
        return
    
    print(f"Found {len(doc_files)} documents\n")
    
    # Start timing
    start_time = time.time()
    
    # Load and process documents
    documents = []
    doc_names = []
    total_words = 0
    
    print("Loading documents...")
    for doc_file in doc_files:
        doc_path = os.path.join(doc_folder, doc_file)
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(content)
                doc_names.append(doc_file)
                # Count words for statistics
                words = len(content.split())
                total_words += words
        except Exception as e:
            print(f"Warning: Could not read {doc_file}: {e}")
    
    load_time = time.time() - start_time
    print(f"✓ Loaded {len(documents)} documents in {load_time:.2f} seconds")
    print(f"  Average document length: {total_words // len(documents)} words\n")
    
    # Calculate TF-IDF (this is done inside search_documents, but we need vocab size)
    print("Calculating TF-IDF...")
    calc_start = time.time()
    
    # Calculate IDF for vocabulary size
    from run_analysis import clean_text
    doc_words = [clean_text(doc) for doc in documents]
    idf_results = calculate_idf(doc_words)
    
    calc_time = time.time() - calc_start
    print(f"✓ TF-IDF calculation completed in {calc_time:.2f} seconds\n")
    
    # Run queries
    print(f"Running {len(queries)} queries...")
    print("-" * 80)
    
    query_results = []
    for i, query in enumerate(queries, 1):
        query_start = time.time()
        results = search_documents(documents, query, doc_names)
        query_time = time.time() - query_start
        
        if results:
            best_doc, best_score, matching_words = results[0]
            query_results.append({
                'query': query,
                'best_doc': best_doc,
                'score': best_score,
                'time': query_time,
                'num_results': len([r for r in results if r[1] > 0])
            })
            
            print(f"Query {i}: {query}")
            print(f"  Best match: {best_doc} (Score: {best_score:.6f})")
            print(f"  Time: {query_time:.4f}s | Relevant docs: {len([r for r in results if r[1] > 0])}")
        else:
            print(f"Query {i}: {query}")
            print(f"  No results found")
        print()
    
    # Summary statistics
    total_time = time.time() - start_time
    avg_query_time = sum(r['time'] for r in query_results) / len(query_results) if query_results else 0
    
    print("="*80)
    print(f" Performance Summary - {dataset_name}")
    print("="*80)
    print(f"Total documents:        {len(documents):,}")
    print(f"Total words:            {total_words:,}")
    print(f"Unique vocabulary:      {len(idf_results):,}")
    print(f"Loading time:           {load_time:.2f}s")
    print(f"TF-IDF calculation:     {calc_time:.2f}s")
    print(f"Total processing time:  {total_time:.2f}s")
    print(f"Average query time:     {avg_query_time:.4f}s")
    print(f"Queries per second:     {len(queries)/total_time:.2f}")
    print("="*80)
    
    return {
        'dataset': dataset_name,
        'num_docs': len(documents),
        'total_words': total_words,
        'vocab_size': len(idf_results),
        'load_time': load_time,
        'calc_time': calc_time,
        'total_time': total_time,
        'avg_query_time': avg_query_time,
        'query_results': query_results
    }

def print_comparison(results_list):
    """Print comparison table between datasets"""
    if len(results_list) < 2:
        return
    
    print("\n" + "="*80)
    print(" Dataset Comparison")
    print("="*80)
    
    # Header
    print(f"{'Metric':<30} {'Sample (10 docs)':<25} {'Full (18K+ docs)':<25}")
    print("-"*80)
    
    metrics = [
        ('Documents', 'num_docs', ','),
        ('Total Words', 'total_words', ','),
        ('Vocabulary Size', 'vocab_size', ','),
        ('Load Time', 'load_time', '.2f'),
        ('TF-IDF Calc Time', 'calc_time', '.2f'),
        ('Total Time', 'total_time', '.2f'),
        ('Avg Query Time', 'avg_query_time', '.4f'),
    ]
    
    for label, key, fmt in metrics:
        val1 = results_list[0][key]
        val2 = results_list[1][key]
        
        if fmt == ',':
            print(f"{label:<30} {val1:>24,} {val2:>24,}")
        else:
            fmt_str = f"{{val:>{24}{fmt}}}"
            val1_str = fmt_str.replace('{val', '{val1').format(val1=val1)
            val2_str = fmt_str.replace('{val', '{val2').format(val2=val2)
            
            if 'Time' in label:
                val1_str += 's'
                val2_str += 's'
            
            print(f"{label:<30} {val1_str} {val2_str}")
    
    # Calculate speedup/slowdown
    print("-"*80)
    speedup = results_list[0]['avg_query_time'] / results_list[1]['avg_query_time'] if results_list[1]['avg_query_time'] > 0 else 0
    if speedup > 1:
        print(f"{'Query Performance':<30} {'Baseline':<25} {f'{speedup:.1f}x faster':<25}")
    else:
        print(f"{'Query Performance':<30} {f'{1/speedup:.1f}x slower':<25} {'Baseline':<25}")
    
    print("="*80)

def main():
    # Test queries
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
    
    # Test 1: Small sample dataset (10 documents)
    sample_folder = "dataset/newsgroups_sample"
    if os.path.exists(sample_folder):
        result1 = run_tfidf_analysis(sample_folder, queries, "Newsgroups Sample (10 docs)")
        if result1:
            results.append(result1)
    
    # Test 2: Full dataset (18,846 documents)
    full_folder = "dataset/newsgroups_full"
    if os.path.exists(full_folder):
        result2 = run_tfidf_analysis(full_folder, queries, "Newsgroups Full (18K+ docs)")
        if result2:
            results.append(result2)
    
    # Print comparison
    if len(results) >= 2:
        print_comparison(results)
    
    print("\n✓ Testing complete!")

if __name__ == "__main__":
    main()
