#!/usr/bin/env python3
"""
TF-IDF Implementation using MRJob
Author: Student
Date: November 2025

This script implements TF-IDF (Term Frequency * Inverse Document Frequency) 
algorithm using MapReduce pattern to rank documents by relevance to search query.

Input: Directory with text files and search query
Output: Files ranked by average TF-IDF score for query terms
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import math
import json
import os
from collections import defaultdict

WORD_RE = re.compile(r'\b[a-zA-Z]+\b')


class TfIdfJob(MRJob):
    """
    MapReduce job to calculate TF-IDF scores for documents.
    
    Steps:
    1. Calculate term frequencies (TF) for each document
    2. Calculate document frequencies (DF) and inverse document frequencies (IDF)  
    3. Compute TF-IDF scores and rank documents
    """
    
    def configure_args(self):
        """Configure command line arguments"""
        super().configure_args()
        self.add_passthru_arg(
            '--query', type=str, required=True,
            help='Search query (space-separated words)'
        )
        self.add_passthru_arg(
            '--docs-dir', type=str, required=True,
            help='Directory containing text files'
        )
    
    def steps(self):
        """Define MapReduce steps"""
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper_count_words,
                   reducer=self.reducer_tf_calculation),
            MRStep(mapper=self.mapper_doc_freq,
                   reducer=self.reducer_idf_calculation),
            MRStep(mapper=self.mapper_tfidf_score,
                   reducer=self.reducer_rank_documents)
        ]
    
    def mapper_init(self):
        """Initialize mapper with query terms"""
        self.query_terms = set(self.options.query.lower().split())
    
    def mapper_count_words(self, filename, content):
        """
        Step 1 Mapper: Count word frequencies in each document
        
        Input: (filename, file_content)
        Output: ((word, filename), count)
        """
        if not filename or not content:
            return
            
        words = WORD_RE.findall(content.lower())
        word_counts = defaultdict(int)
        
        for word in words:
            if word in self.query_terms:
                word_counts[word] += 1
        
        total_words = len(words)
        
        for word, count in word_counts.items():
            tf = count / total_words if total_words > 0 else 0
            yield ((word, filename), tf)
    
    def reducer_tf_calculation(self, word_file, tf_values):
        """
        Step 1 Reducer: Aggregate TF values
        
        Input: ((word, filename), [tf_values])
        Output: ((word, filename), tf_score)
        """
        tf_score = sum(tf_values)
        yield ((word_file[0], word_file[1]), tf_score)
    
    def mapper_doc_freq(self, word_file, tf_score):
        """
        Step 2 Mapper: Prepare for document frequency calculation
        
        Input: ((word, filename), tf_score)
        Output: (word, (filename, tf_score))
        """
        word, filename = word_file
        yield (word, (filename, tf_score))
    
    def reducer_idf_calculation(self, word, file_tf_pairs):
        """
        Step 2 Reducer: Calculate IDF and emit TF-IDF scores
        
        Input: (word, [(filename, tf_score), ...])
        Output: (filename, (word, tfidf_score))
        """
        file_tf_list = list(file_tf_pairs)
        doc_freq = len(file_tf_list)  # Number of documents containing the word
        
        # Estimate total documents (this is simplified)
        total_docs = max(10, doc_freq * 2)  # Simple estimation
        idf = math.log(total_docs / doc_freq) if doc_freq > 0 else 0
        
        for filename, tf_score in file_tf_list:
            tfidf_score = tf_score * idf
            yield (filename, (word, tfidf_score))
    
    def mapper_tfidf_score(self, filename, word_tfidf):
        """
        Step 3 Mapper: Pass through TF-IDF scores
        
        Input: (filename, (word, tfidf_score))
        Output: (filename, (word, tfidf_score))
        """
        yield (filename, word_tfidf)
    
    def reducer_rank_documents(self, filename, word_tfidf_pairs):
        """
        Step 3 Reducer: Calculate average TF-IDF and rank documents
        
        Input: (filename, [(word, tfidf_score), ...])
        Output: (avg_tfidf_score, filename) - sorted by score
        """
        tfidf_scores = [score for word, score in word_tfidf_pairs]
        
        if tfidf_scores:
            avg_tfidf = sum(tfidf_scores) / len(tfidf_scores)
            # Negative score for reverse sorting (highest first)
            yield (-avg_tfidf, filename)


if __name__ == '__main__':
    TfIdfJob.run()