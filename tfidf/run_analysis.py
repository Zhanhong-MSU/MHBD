#!/usr/bin/env python3
"""
TF-IDF Analysis - Complete Implementation
Document Collection Analysis using TF-IDF Algorithm
Standalone implementation with Python standard library only (Python 3.6+)

Author: Student Submission
Date: November 2025
"""

import os
import sys
import re
import math
from collections import defaultdict, Counter

def clean_text(text):
    """
    Clean and tokenize text into words.
    
    Args:
        text (str): Input text to be cleaned
        
    Returns:
        list: List of lowercase words (alphabetic characters only)
    """
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def calculate_tf(word_list):
    """
    Calculate Term Frequency (TF) for each word in the document.
    TF = (Number of times term appears in document) / (Total number of terms in document)
    
    Args:
        word_list (list): List of words in the document
        
    Returns:
        dict: Dictionary mapping each word to its TF value
    """
    word_count = len(word_list)
    tf_dict = {}
    counter = Counter(word_list)
    
    for word, count in counter.items():
        tf_dict[word] = count / word_count
    
    return tf_dict

def calculate_idf(documents):
    """
    Calculate Inverse Document Frequency (IDF) for all words across documents.
    IDF = log(Total number of documents / Number of documents containing the term)
    
    Args:
        documents (list): List of tokenized documents (each document is a list of words)
        
    Returns:
        dict: Dictionary mapping each word to its IDF value
    """
    total_docs = len(documents)
    idf_dict = {}
    all_words = set(word for doc in documents for word in doc)
    
    for word in all_words:
        docs_containing_word = sum(1 for doc in documents if word in doc)
        idf_dict[word] = math.log(total_docs / docs_containing_word)
    
    return idf_dict

def print_table_header():
    """Print formatted table header for query results summary."""
    print("\n📊 QUERY RESULTS SUMMARY TABLE")
    print("=" * 110)
    print(f"{'Rank':<4} {'Document':<40} {'Query':<35} {'Score':<8} {'Key Terms':<18}")
    print("=" * 110)

def print_table_row(rank, doc_name, query, score, top_terms):
    """
    Print a formatted table row with query results.
    
    Args:
        rank (int): Result ranking position
        doc_name (str): Document filename
        query (str): Query string
        score (float): TF-IDF relevance score
        top_terms (str): Top matching terms
    """
    # Clean document name (remove .txt extension and shorten for display)
    doc_clean = doc_name.replace('.txt', '').replace('_', ' ').title()
    doc_short = doc_clean[:37] + "..." if len(doc_clean) > 40 else doc_clean
    
    # Shorten query and top terms for better table fit
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
    """
    Calculate star rating based on average TF-IDF score.
    
    Args:
        avg_score (float): Average TF-IDF score for a document
        
    Returns:
        str: Star rating (⭐ to ⭐⭐⭐⭐⭐)
    """
    if avg_score >= 0.020:
        return "⭐⭐⭐⭐⭐"
    elif avg_score >= 0.015:
        return "⭐⭐⭐⭐"
    elif avg_score >= 0.010:
        return "⭐⭐⭐"
    elif avg_score >= 0.005:
        return "⭐⭐"
    else:
        return "⭐"

def search_documents(documents, query, doc_names):
    """
    Search and rank documents using TF-IDF algorithm.
    
    Args:
        documents (list): List of document contents (strings)
        query (str): Search query string
        doc_names (list): List of document filenames
        
    Returns:
        list: Sorted list of tuples (doc_name, score, matching_words)
              where matching_words contains (word, tf, idf, tfidf) tuples
    """
    # Tokenize all documents
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

def run_tfidf_analysis(dataset='sample'):
    """
    Execute TF-IDF analysis on document collection.
    
    Args:
        dataset (str): Dataset to analyze - 'sample' (10 docs) or 'full' (17,901 docs)
        
    Returns:
        bool: True if analysis completed successfully, False otherwise
    """
    # Initialize document storage
    documents = []
    doc_names = []
    
    # Choose dataset directory based on parameter
    if dataset == 'full':
        documents_dir = 'documents/newsgroups_full'
    else:
        documents_dir = 'documents/newsgroups_sample'
    
    if not os.path.exists(documents_dir):
        print(f"❌ Error: {documents_dir} directory not found")
        return False
    
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
                print(f"❌ Error reading {filename}: {e}")
                return False
    
    if not documents:
        print("❌ No documents found in the documents directory")
        return False
    
    print("📊 TF-IDF Algorithm Results")
    print("=" * 100)
    
    # Display document overview table
    print("\n📋 DOCUMENT OVERVIEW")
    print("-" * 80)
    print(f"{'#':<3} {'Document':<40} {'Size':<12} {'Topic':<25}")
    print("-" * 80)
    
    # Topic mapping for document categorization
    topics = {
        "paper1_machine_learning.txt": "Healthcare ML",
        "paper2_deep_learning.txt": "NLP & Deep Learning", 
        "paper3_data_science.txt": "Business Analytics",
        "paper4_artificial_intelligence.txt": "AI Ethics",
        "paper5_computer_vision.txt": "Computer Vision & Robotics",
        # 20 Newsgroups dataset categories
        "doc1_comp_graphics.txt": "Computer Graphics",
        "doc2_comp_graphics.txt": "Computer Graphics",
        "doc3_sci_med.txt": "Medical Science",
        "doc4_talk_politics_misc.txt": "Politics",
        "doc5_sci_med.txt": "Medical Science",
        "doc6_talk_politics_misc.txt": "Politics",
        "doc7_alt_atheism.txt": "Religion/Atheism",
        "doc8_sci_med.txt": "Medical Science",
        "doc9_comp_graphics.txt": "Computer Graphics",
        "doc10_rec_sport_baseball.txt": "Sports/Baseball"
    }
    
    for i, (name, content) in enumerate(zip(doc_names, documents), 1):
        word_count = len(content.split())
        doc_clean = name.replace('.txt', '').replace('_', ' ').title()
        doc_short = doc_clean[:37] + "..." if len(doc_clean) > 40 else doc_clean
        topic = topics.get(name, "General")
        print(f"{i:<3} {doc_short:<40} {word_count:>4} words   {topic:<25}")
    
    print("-" * 80)
    print()
    
    # Display preview of document contents
    print(f"📄 Document Content Preview:")
    for i, (name, content) in enumerate(zip(doc_names, documents), 1):
        # Display first 80 characters of each document
        preview = content[:80] + "..." if len(content) > 80 else content
        print(f"{i}. {name}: {preview}")
    print()
    
    # Define test queries for newsgroups dataset
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
    
    # Store results for summary table
    all_results = []
    
    # Execute TF-IDF analysis for each query
    print("🔍 DETAILED QUERY ANALYSIS")
    print("=" * 100)
    
    for query in queries:
        print(f"\n🔎 Query: '{query}'")
        print("-" * 50)
        
        results = search_documents(documents, query, doc_names)
        
        for rank, (doc_name, score, matching_words) in enumerate(results, 1):
            print(f"{rank}. {doc_name} (Score: {score:.4f})")
            
            if matching_words:
                print("   Matching terms:")
                for word, tf_val, idf_val, tfidf in matching_words:
                    print(f"     '{word}': TF={tf_val:.4f}, IDF={idf_val:.4f}, TF-IDF={tfidf:.4f}")
            else:
                print("   (No matching terms found)")
            
            # Store top result for each query in summary table
            if rank == 1:
                top_terms = ", ".join([word for word, _, _, _ in matching_words[:3]]) if matching_words else "None"
                all_results.append((rank, doc_name, query, score, top_terms))
    
    print("\n" + "=" * 100)
    
    # Display summary table with top results
    print_table_header()
    for result in all_results:
        print_table_row(*result)
    print("=" * 110)
    
    # Overall statistics
    print(f"\n📈 ANALYSIS STATISTICS")
    print(f"• Total Queries Processed: {len(queries)}")
    print(f"• Total Documents Analyzed: {len(documents)}")
    print(f"• Score Range: {min(r[3] for r in all_results):.4f} - {max(r[3] for r in all_results):.4f}")
    print(f"• Best Match: {max(all_results, key=lambda x: x[3])[1]} (Score: {max(r[3] for r in all_results):.4f})")
    
    # Document performance summary
    print_performance_table_header()
    doc_counts = {}
    for _, doc_name, _, score, _ in all_results:
        if doc_name not in doc_counts:
            doc_counts[doc_name] = {"count": 0, "total_score": 0}
        doc_counts[doc_name]["count"] += 1
        doc_counts[doc_name]["total_score"] += score
    
    # Sort by average score
    doc_ranking = []
    for doc_name, stats in doc_counts.items():
        avg_score = stats["total_score"] / stats["count"]
        doc_ranking.append((doc_name, stats["count"], avg_score))
    
    doc_ranking.sort(key=lambda x: x[2], reverse=True)
    
    for i, (doc_name, count, avg_score) in enumerate(doc_ranking, 1):
        # Clean document name for display
        doc_clean = doc_name.replace('.txt', '').replace('_', ' ').title()
        doc_short = doc_clean[:42] + "..." if len(doc_clean) > 45 else doc_clean
        rating = get_performance_rating(avg_score)
        print(f"{i:<4} {doc_short:<45} {count:<6} {avg_score:<10.4f} {rating:<10}")
    
    print("=" * 80)
    
    return True

def main():
    """
    Main function to execute TF-IDF analysis.
    Handles command-line arguments and orchestrates the analysis workflow.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    # Parse command-line arguments
    dataset = 'sample'  # Default to sample dataset
    if len(sys.argv) > 1:
        if sys.argv[1] in ['sample', 'full']:
            dataset = sys.argv[1]
        else:
            print("Usage: python run_analysis.py [sample|full]")
            print("  sample: Run on 10-document sample dataset (default)")
            print("  full:   Run on complete 17,901-document dataset")
            return 1
    
    print("="*80)
    print("📊 TF-IDF ALGORITHM DEMONSTRATION")
    print(f"Dataset: {'20 Newsgroups Sample (10 docs)' if dataset == 'sample' else '20 Newsgroups Full (17,901 docs)'}")
    print("="*80)
    print()
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return 1
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    print()
    
    # Display document collection information
    if dataset == 'full':
        documents_dir = 'documents/newsgroups_full'
    else:
        documents_dir = 'documents/newsgroups_sample'
    
    if not os.path.exists(documents_dir):
        print(f"❌ Error: {documents_dir} directory not found")
        return 1
        
    print(f"📚 Document Collection ({documents_dir}/):")
    print("-" * 50)
    
    doc_count = 0
    total_words = 0
    
    try:
        # Count documents and calculate statistics
        for filename in sorted(os.listdir(documents_dir)):
            if filename.endswith('.txt'):
                filepath = os.path.join(documents_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    word_count = len(content.split())
                    total_words += word_count
                    doc_count += 1
                    
                    # Display document information (title from first line)
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
    
    # Execute TF-IDF analysis on selected dataset
    try:
        success = run_tfidf_analysis(dataset=dataset)
        if not success:
            return 1
            
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("="*80)
    print("✅ ANALYSIS COMPLETE")
    if dataset == 'sample':
        print("This demonstrates TF-IDF algorithm on 10 newsgroups sample documents")
        print("covering Computer Graphics, Medical Science, Politics, Baseball, and Atheism.")
    else:
        print("This demonstrates TF-IDF algorithm on complete 20 Newsgroups dataset")
        print("with 17,901 documents across 20 different categories.")
    print("="*80)
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)