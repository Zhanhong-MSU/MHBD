#!/usr/bin/env python3
"""
TF-IDF Analysis - MapReduce Version (using mrjob)
This script prepares the data and runs the MapReduce job defined in tfidf.py.

Features:
- Prepares input data for MapReduce (combines files into one input)
- Runs the MRJob process
- Parses output and performs search queries
"""

import os
import sys
import time
import shutil
import argparse
from collections import defaultdict
from tfidf import MRTFIDF  # Import the MRJob class

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

def prepare_input_file(documents_dir, output_file):
    """
    Reads all .txt files in documents_dir and writes them to a single file
    in the format: "filename <tab> content"
    """
    print(f"📂 Scanning directory {documents_dir}...")
    
    if not os.path.exists(documents_dir):
        print(f"❌ Error: {documents_dir} directory not found")
        return 0

    count = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in sorted(os.listdir(documents_dir)):
            if filename.endswith('.txt'):
                filepath = os.path.join(documents_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as infile:
                        content = infile.read().strip().replace('\n', ' ').replace('\t', ' ')
                        if content:
                            outfile.write(f"{filename}\t{content}\n")
                            count += 1
                except Exception as e:
                    print(f"⚠️ Warning: Could not read {filename}: {e}")
    
    print(f"✅ Prepared {count} documents in {output_file}")
    return count

def run_mr_analysis(dataset='sample', search_query=None):
    start_time = time.time()
    
    # 1. Setup Paths
    # Get absolute path to the current script directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    if dataset == 'full':
        documents_dir = os.path.join(base_dir, 'dataset/newsgroups_full')
    else:
        documents_dir = os.path.join(base_dir, 'dataset/sample')
        
    input_file = os.path.join(base_dir, 'tfidf_input.txt')
    
    # 2. Prepare Data
    print("⚙️  Step 1: Preparing input data for MapReduce...")
    total_docs = prepare_input_file(documents_dir, input_file)
    
    if total_docs == 0:
        print("❌ No documents found. Please check your dataset.")
        return

    # 3. Run MapReduce Job
    print(f"⚙️  Step 2: Running MapReduce Job (mrjob)...")
    mr_start_time = time.time()
    
    # We run the job programmatically
    mr_job = MRTFIDF(args=[input_file, f'--total-docs={total_docs}'])
    
    # Store results: doc_vectors[filename] = {word: score}
    doc_vectors = defaultdict(dict)
    
    with mr_job.make_runner() as runner:
        runner.run()
        for key, value in mr_job.parse_output(runner.cat_output()):
            # key is filename, value is [word, score]
            filename = key
            word, score = value
            doc_vectors[filename][word] = score
            
    mr_time = time.time() - mr_start_time
    print(f"   ✅ MapReduce complete in {mr_time:.2f} seconds")

    # 4. Perform Search Queries (Client-side)
    print(f"⚙️  Step 3: Performing Search Queries...")
    
    if search_query:
        queries = [search_query]
        print(f"\n🔍 Performing Search for: '{search_query}'")
    else:
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
        print("\n🔍 QUERY RESULTS")
        print("=" * 100)
    
    all_results = []

    for query in queries:
        if not search_query:
            print(f"\n🔎 Query: '{query}'")
            
        query_words = query.lower().split()
        
        # Score documents against query
        scores = []
        for filename, vector in doc_vectors.items():
            score = 0.0
            matching_terms = []
            
            for q_word in query_words:
                if q_word in vector:
                    term_score = vector[q_word]
                    score += term_score
                    matching_terms.append(f"{q_word}({term_score:.4f})")
            
            if score > 0:
                # Average score by query length (optional, but consistent with previous logic)
                avg_score = score / len(query_words)
                scores.append((filename, avg_score, matching_terms))
        
        # Sort and display top 5
        scores.sort(key=lambda x: x[1], reverse=True)
        
        if search_query:
             # Print simple list for single query as per assignment requirement
             print(f"\nResults sorted by Average TF-IDF Score:")
             print(f"{'Rank':<5} {'Document':<40} {'Score':<10}")
             print("-" * 60)
             for i, (fname, score, terms) in enumerate(scores, 1):
                 print(f"{i:<5} {fname:<40} {score:.4f}")
        else:
            if not scores:
                print("   No matching documents found.")
            else:
                for i, (fname, score, terms) in enumerate(scores[:5], 1):
                    print(f"   {i}. {fname} (Score: {score:.4f})")
                    print(f"      Matches: {', '.join(terms)}")
                    
                    if i == 1:
                        # Extract just the words from "word(score)" format for the summary table
                        clean_terms = ", ".join([t.split('(')[0] for t in terms[:3]])
                        all_results.append((i, fname, query, score, clean_terms))

    # Cleanup
    if os.path.exists(input_file):
        os.remove(input_file)
        
    total_time = time.time() - start_time
    print("\n" + "=" * 100)
    print(f"⏱️  Total execution time: {total_time:.2f} seconds")
    
    if not search_query:
        print_table_header()
        for result in all_results:
            print_table_row(*result)
        print("=" * 110)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TF-IDF MapReduce Analysis')
    parser.add_argument('dataset', nargs='?', default='sample', choices=['sample', 'full'], help='Dataset to use (sample or full)')
    parser.add_argument('query', nargs='*', help='Search query words (optional)')
    
    args = parser.parse_args()
    
    search_query = " ".join(args.query) if args.query else None
        
    print("="*80)
    print(f"📊 TF-IDF MAPREDUCE ANALYSIS (mrjob)")
    print(f"Dataset: {args.dataset}")
    if search_query:
        print(f"Query: {search_query}")
    print("="*80)
    
    run_mr_analysis(args.dataset, search_query)
