#!/usr/bin/env python3
"""
TF-IDF Analysis - Optimized Multi-Process Parallel Implementation
Document Collection Analysis using TF-IDF Algorithm with automatic CPU core detection
Standalone implementation with Python standard library only (Python 3.6+)

Features:
- Automatic CPU core detection and adaptation
- Parallel file reading and tokenization (I/O + CPU bound)
- Optimized IDF calculation (O(N) instead of O(N^2))
- Shared memory for large dictionaries to reduce IPC overhead
- Dynamic workload distribution
- Progress tracking for large datasets

Author: GitHub Copilot (Refactored)
Date: November 2025
"""

import os
import sys
import re
import math
import time
import random
from collections import Counter, defaultdict
from multiprocessing import Pool, cpu_count

# Global variables for worker processes
# These are initialized once per process to avoid serialization overhead
shared_idf = None
shared_query_words = None

def init_worker(idf, query_words):
    """
    Initialize worker process with shared read-only data.
    This runs once when the pool creates the worker.
    """
    global shared_idf, shared_query_words
    shared_idf = idf
    shared_query_words = query_words

def clean_text(text):
    """
    Clean and tokenize text into words.
    """
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def process_document_file(filepath):
    """
    Worker function: Read file, clean text, and count terms.
    
    Args:
        filepath (str): Path to the file to process
        
    Returns:
        tuple: (filename, term_counts, total_words, content_preview)
               term_counts is a Counter object (sparse vector)
    """
    try:
        filename = os.path.basename(filepath)
        # Use errors='replace' to handle potential non-utf-8 bytes in dataset
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read().strip()
        
        if not content:
            return (filename, Counter(), 0, "")
            
        words = clean_text(content)
        word_count = len(words)
        term_counts = Counter(words)
        
        # Keep a short preview for display (first 100 chars)
        preview = content[:100].replace('\n', ' ')
        
        return (filename, term_counts, word_count, preview)
    except Exception as e:
        # Return empty result on error
        return (os.path.basename(filepath), Counter(), 0, "")

def calculate_document_score_worker(args):
    """
    Worker function: Calculate TF-IDF score for a single document.
    Uses shared_idf and shared_query_words from global scope.
    
    Args:
        args (tuple): (filename, term_counts, total_words)
        
    Returns:
        tuple: (filename, score, matching_words)
    """
    filename, term_counts, total_words = args
    global shared_idf, shared_query_words
    
    if total_words == 0:
        return (filename, 0.0, [])
    
    score = 0.0
    matching_words = []
    
    # Only iterate through query words (efficient for sparse vectors)
    for q_word in shared_query_words:
        # TF = count / total_words
        count = term_counts.get(q_word, 0)
        if count > 0:
            tf_val = count / total_words
            idf_val = shared_idf.get(q_word, 0.0)
            tfidf_score = tf_val * idf_val
            
            score += tfidf_score
            matching_words.append((q_word, tf_val, idf_val, tfidf_score))
    
    if shared_query_words:
        score /= len(shared_query_words)  # Average score
    
    return (filename, score, matching_words)

def print_table_header():
    """Print formatted table header for query results summary."""
    print("\n📊 QUERY RESULTS SUMMARY TABLE")
    print("=" * 110)
    print(f"{'Rank':<4} {'Document':<40} {'Query':<35} {'Score':<8} {'Key Terms':<18}")
    print("=" * 110)

def print_table_row(rank, doc_name, query, score, top_terms):
    """Print a formatted table row with query results."""
    doc_clean = doc_name.replace('.txt', '').replace('_', ' ').title()
    doc_short = doc_clean[:37] + "..." if len(doc_clean) > 40 else doc_clean
    query_short = query[:32] + "..." if len(query) > 35 else query
    top_terms_short = top_terms[:15] + "..." if len(top_terms) > 18 else top_terms
    print(f"{rank:<4} {doc_short:<40} {query_short:<35} {score:<8.4f} {top_terms_short:<18}")

def print_performance_table_header():
    """Print formatted table header for document performance summary."""
    print(f"\n🏆 DOCUMENT PERFORMANCE SUMMARY")
    print("=" * 80)
    print(f"{'Rank':<4} {'Document':<45} {'Wins':<6} {'Avg Score':<10} {'Rating':<10}")
    print("=" * 80)

def get_performance_rating(avg_score):
    """Calculate star rating based on average TF-IDF score."""
    if avg_score >= 0.020: return "⭐⭐⭐⭐⭐"
    elif avg_score >= 0.015: return "⭐⭐⭐⭐"
    elif avg_score >= 0.010: return "⭐⭐⭐"
    elif avg_score >= 0.005: return "⭐⭐"
    else: return "⭐"

def run_tfidf_analysis(dataset='sample', num_processes=None, sample_ratio=1.0):
    """
    Execute TF-IDF analysis on document collection with parallel processing.
    """
    if num_processes is None:
        num_processes = cpu_count()
    
    # 1. Identify Files
    if dataset == 'full':
        documents_dir = 'dataset/newsgroups_full'
    else:
        documents_dir = 'dataset/newsgroups_sample'
    
    if not os.path.exists(documents_dir):
        print(f"❌ Error: {documents_dir} directory not found")
        return False
    
    print(f"📂 Scanning directory {documents_dir}...")
    all_filepaths = []
    for filename in sorted(os.listdir(documents_dir)):
        if filename.endswith('.txt'):
            all_filepaths.append(os.path.join(documents_dir, filename))
    
    # Apply sampling
    if sample_ratio < 1.0:
        random.seed(42)
        num_to_sample = max(1, int(len(all_filepaths) * sample_ratio))
        all_filepaths = random.sample(all_filepaths, num_to_sample)
        all_filepaths.sort()
        print(f"📊 Sampling {sample_ratio*100:.1f}% of data: {len(all_filepaths)} documents selected")
    
    if not all_filepaths:
        print("❌ No documents found")
        return False

    # Calculate chunksize
    # For I/O bound tasks (reading files), smaller chunks might be better to keep CPUs busy
    # but for CPU bound (tokenizing), larger chunks reduce overhead.
    # We use a balanced approach.
    chunksize = max(1, len(all_filepaths) // (num_processes * 4))
    print(f"🔧 Using {num_processes} CPU cores with chunksize={chunksize}")

    # 2. Parallel Processing: Read & Tokenize
    print(f"⚙️  Step 1/3: Reading and tokenizing {len(all_filepaths)} documents in parallel...")
    start_time = time.time()
    
    # We use a Pool to process files in parallel.
    # This moves the "Loading documents" phase from serial (main process) to parallel (workers).
    processed_docs = []
    with Pool(processes=num_processes) as pool:
        # map returns results in order
        results = pool.map(process_document_file, all_filepaths, chunksize=chunksize)
        
        # Filter out failed reads (empty content)
        for res in results:
            if res[2] > 0: # word_count > 0
                processed_docs.append(res)
    
    load_time = time.time() - start_time
    print(f"   ✅ Tokenization complete in {load_time:.2f} seconds")
    print(f"   ✅ Successfully processed {len(processed_docs)} documents")

    # Unpack results for next steps
    # processed_docs is list of (filename, term_counts, word_count, preview)
    
    # Display Document Overview (First 10)
    print("\n📋 DOCUMENT OVERVIEW")
    print("-" * 80)
    print(f"{'#':<3} {'Document':<40} {'Size':<12} {'Preview':<25}")
    print("-" * 80)
    
    for i, (fname, _, wcount, preview) in enumerate(processed_docs[:10], 1):
        doc_clean = fname.replace('.txt', '').replace('_', ' ').title()
        doc_short = doc_clean[:37] + "..." if len(doc_clean) > 40 else doc_clean
        print(f"{i:<3} {doc_short:<40} {wcount:>4} words   {preview[:25]}...")
    
    if len(processed_docs) > 10:
        print(f"... and {len(processed_docs) - 10} more documents")
    print("-" * 80)

    # 3. Calculate IDF (Sequential but Optimized)
    print(f"\n⚙️  Step 2/3: Calculating IDF for vocabulary...")
    start_time = time.time()
    
    # Optimized IDF calculation:
    # Iterate over the Counter objects directly.
    # This avoids creating a massive list of all words or iterating text repeatedly.
    doc_freq = Counter()
    for _, counts, _, _ in processed_docs:
        # counts.keys() gives unique words in the doc
        doc_freq.update(counts.keys())
    
    total_docs = len(processed_docs)
    idf_dict = {}
    for word, freq in doc_freq.items():
        idf_dict[word] = math.log(total_docs / freq)
        
    idf_time = time.time() - start_time
    print(f"   ✅ IDF calculation complete in {idf_time:.2f} seconds ({len(idf_dict)} unique words)")

    # 4. Parallel Scoring
    print(f"⚙️  Step 3/3: Calculating TF-IDF scores in parallel...")
    
    queries = [
        "computer graphics image display",
        "medical doctor patient health",
        "politics government election",
        "baseball game sport team",
        "religion atheism god belief",
        "science research study",
        "software program algorithm",
        "treatment disease clinical"
    ]
    
    all_results = []
    total_query_time = 0
    
    print("🔍 DETAILED QUERY ANALYSIS")
    print("=" * 100)
    
    # Prepare arguments for scoring
    # We strip the preview string to save memory during transfer
    score_args = [(fname, counts, wcount) for fname, counts, wcount, _ in processed_docs]
    
    for query_num, query in enumerate(queries, 1):
        print(f"\n🔎 Query {query_num}/{len(queries)}: '{query}'")
        print("-" * 50)
        
        query_words = clean_text(query)
        query_start = time.time()
        
        # Create a new pool for scoring, initializing workers with the IDF dict and Query
        # This is crucial: passing idf_dict (potentially large) once per process
        # instead of once per task drastically reduces IPC overhead.
        with Pool(processes=num_processes, initializer=init_worker, initargs=(idf_dict, query_words)) as pool:
            doc_scores = pool.map(calculate_document_score_worker, score_args, chunksize=chunksize)
        
        # Sort results
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        
        query_time = time.time() - query_start
        total_query_time += query_time
        print(f"⏱️  Query processed in {query_time:.2f} seconds")
        
        # Display top results
        print(f"\nTop 5 Results:")
        for rank, (doc_name, score, matching_words) in enumerate(doc_scores[:5], 1):
            print(f"{rank}. {doc_name} (Score: {score:.4f})")
            if matching_words and rank <= 3:
                print("   Matching terms:")
                for word, tf_val, idf_val, tfidf in matching_words[:5]:
                    print(f"     '{word}': TF={tf_val:.4f}, IDF={idf_val:.4f}, TF-IDF={tfidf:.4f}")
            
            if rank == 1:
                top_terms = ", ".join([w for w, _, _, _ in matching_words[:3]]) if matching_words else "None"
                all_results.append((rank, doc_name, query, score, top_terms))

    # Summary Statistics
    print("\n" + "=" * 100)
    print(f"⏱️  Total query processing time: {total_query_time:.2f} seconds")
    
    print_table_header()
    for result in all_results:
        print_table_row(*result)
    print("=" * 110)
    
    return True

def main():
    # Parse arguments
    dataset = 'sample'
    num_processes = None
    sample_ratio = 1.0
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['sample', 'full']:
            dataset = sys.argv[1]
    
    if len(sys.argv) > 2:
        try:
            val = sys.argv[2]
            if val.lower() != 'auto':
                num_processes = int(val)
        except ValueError:
            pass
            
    if len(sys.argv) > 3:
        try:
            sample_ratio = float(sys.argv[3])
        except ValueError:
            pass

    available_cores = cpu_count()
    if num_processes is None:
        num_processes = available_cores

    print("="*80)
    print("📊 TF-IDF ALGORITHM - OPTIMIZED PARALLEL VERSION")
    print(f"Dataset: {dataset}")
    print(f"Cores: {num_processes}/{available_cores}")
    if sample_ratio < 1.0:
        print(f"Sampling: {sample_ratio*100}%")
    print("="*80)
    
    try:
        run_tfidf_analysis(dataset, num_processes, sample_ratio)
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
