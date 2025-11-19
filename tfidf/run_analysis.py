#!/usr/bin/env python3
"""
TF-IDF Analysis - Complete Implementation
Academic Paper Document Collection Analysis
Standalone version with full TF-IDF algorithm implementation
Works on any VPS with Python 3.6+
"""

import os
import sys
import re
import math
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

def print_table_header():
    """Print a formatted table header"""
    print("\n📊 QUERY RESULTS SUMMARY TABLE")
    print("=" * 110)
    print(f"{'Rank':<4} {'Document':<40} {'Query':<35} {'Score':<8} {'Key Terms':<18}")
    print("=" * 110)

def print_table_row(rank, doc_name, query, score, top_terms):
    """Print a formatted table row"""
    # Clean document name (remove .txt extension and shorten)
    doc_clean = doc_name.replace('.txt', '').replace('_', ' ').title()
    doc_short = doc_clean[:37] + "..." if len(doc_clean) > 40 else doc_clean
    
    # Shorten query and top terms for better table fit
    query_short = query[:32] + "..." if len(query) > 35 else query
    top_terms_short = top_terms[:15] + "..." if len(top_terms) > 18 else top_terms
    
    print(f"{rank:<4} {doc_short:<40} {query_short:<35} {score:<8.4f} {top_terms_short:<18}")

def print_performance_table_header():
    """Print document performance table header"""
    print(f"\n🏆 DOCUMENT PERFORMANCE SUMMARY")
    print("=" * 80)
    print(f"{'Rank':<4} {'Document':<45} {'Wins':<6} {'Avg Score':<10} {'Rating':<10}")
    print("=" * 80)

def get_performance_rating(avg_score):
    """Get performance rating based on average score"""
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

def run_tfidf_analysis():
    """Run the TF-IDF analysis on documents"""
    # Read documents from documents directory
    documents = []
    doc_names = []
    documents_dir = 'documents'
    
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
    
    # Quick overview table
    print("\n📋 DOCUMENT OVERVIEW")
    print("-" * 80)
    print(f"{'#':<3} {'Document':<40} {'Size':<12} {'Topic':<25}")
    print("-" * 80)
    
    topics = {
        "paper1_machine_learning.txt": "Healthcare ML",
        "paper2_deep_learning.txt": "NLP & Deep Learning", 
        "paper3_data_science.txt": "Business Analytics",
        "paper4_artificial_intelligence.txt": "AI Ethics",
        "paper5_computer_vision.txt": "Computer Vision & Robotics"
    }
    
    for i, (name, content) in enumerate(zip(doc_names, documents), 1):
        word_count = len(content.split())
        doc_clean = name.replace('.txt', '').replace('_', ' ').title()
        doc_short = doc_clean[:37] + "..." if len(doc_clean) > 40 else doc_clean
        topic = topics.get(name, "Unknown")
        print(f"{i:<3} {doc_short:<40} {word_count:>4} words   {topic:<25}")
    
    print("-" * 80)
    print()
    
    # Display document summary for detailed view
    print(f"📄 Document Content Preview:")
    for i, (name, content) in enumerate(zip(doc_names, documents), 1):
        # Show first 80 characters of each document for better table formatting
        preview = content[:80] + "..." if len(content) > 80 else content
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
    
    # Store all results for summary table
    all_results = []
    
    # Run detailed analysis for each query
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
            
            # Store for summary table (only top result per query)
            if rank == 1:
                top_terms = ", ".join([word for word, _, _, _ in matching_words[:3]]) if matching_words else "None"
                all_results.append((rank, doc_name, query, score, top_terms))
    
    print("\n" + "=" * 100)
    
    # Print summary table
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
    print("="*80)
    print("📊 TF-IDF ALGORITHM DEMONSTRATION")
    print("Academic Paper Document Collection Analysis")
    print("="*80)
    print()
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return 1
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    print()
    
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
    
    # Run TF-IDF analysis
    try:
        success = run_tfidf_analysis()
        if not success:
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