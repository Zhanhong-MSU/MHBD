from mrjob.job import MRJob
from mrjob.step import MRStep
import math
import re

class MRTFIDF(MRJob):
    """
    A MapReduce job to calculate TF-IDF scores for documents.
    
    Input Format:
        Each line should be: "filename <tab> document_content"
    
    Output Format:
        key: filename
        value: [word, tfidf_score]
    """

    def configure_args(self):
        super(MRTFIDF, self).configure_args()
        self.add_passthru_arg('--total-docs', type=int, help='Total number of documents in the corpus')

    def steps(self):
        return [
            # Step 1: Calculate Term Frequency (TF) per document
            MRStep(mapper=self.mapper_get_words,
                   reducer=self.reducer_count_tf),
            # Step 2: Calculate Document Frequency (DF) and TF-IDF
            MRStep(reducer=self.reducer_calculate_tfidf)
        ]

    def mapper_get_words(self, _, line):
        """
        Mapper 1: Tokenize document content.
        Input: "filename <tab> content"
        Output: filename, word
        """
        try:
            # Split only on the first tab to separate filename from content
            if '\t' in line:
                filename, content = line.split('\t', 1)
                # Simple tokenization: lowercase and keep only letters
                words = re.findall(r'\b[a-zA-Z]+\b', content.lower())
                for word in words:
                    yield filename, word
        except ValueError:
            pass

    def reducer_count_tf(self, filename, words):
        """
        Reducer 1: Calculate TF for each word in a document.
        Input: filename, [word, word, ...]
        Output: word, (filename, tf)
        """
        # Count word frequencies for this document
        word_counts = {}
        total_words = 0
        
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
            total_words += 1
        
        if total_words > 0:
            for word, count in word_counts.items():
                tf = count / total_words
                # Emit word as key so we can group by word in the next step to calculate DF
                yield word, (filename, tf)

    def reducer_calculate_tfidf(self, word, doc_tf_pairs):
        """
        Reducer 2: Calculate IDF and then TF-IDF.
        Input: word, [(filename, tf), (filename, tf), ...]
        Output: filename, (word, tfidf_score)
        """
        # doc_tf_pairs is a generator, convert to list to count DF
        doc_list = list(doc_tf_pairs)
        df = len(doc_list)
        
        # Get total documents from command line argument
        total_docs = self.options.total_docs
        
        if total_docs and df > 0:
            # IDF formula: log(Total Documents / Document Frequency)
            idf = math.log(total_docs / df)
            
            for filename, tf in doc_list:
                tfidf_score = tf * idf
                # Emit filename as key to group results by document
                yield filename, (word, tfidf_score)

if __name__ == '__main__':
    MRTFIDF.run()
