# TF-IDF MapReduce Implementation

This project implements TF-IDF using the `mrjob` library.

## 📋 Files

- `tfidf.py`: The MapReduce job class (Mapper & Reducer).
- `run.py`: The driver script that runs the job and formats the output.
- `dataset/`: Contains the document sets.
- `manage_dataset.py`: Helper script to download the full dataset.

## 🚀 Usage

### Prerequisites
```bash
pip install -r requirements.txt
```

### 1. Run with Specific Query (Assignment Requirement)
To search for a term and get a ranked list of documents:
```bash
python3 run.py sample "computer science"
```

**Output Format:**
```
Rank  Document                                 Score     
------------------------------------------------------------
1     doc1_comp_graphics.txt                   0.0071
...
```

### 2. Run Default Test Suite
Runs a set of predefined queries to verify functionality:
```bash
python3 run.py
```

### 3. Use Full Dataset
To download and run on the full 20 Newsgroups dataset:
```bash
# Download data
python3 manage_dataset.py download

# Run analysis
python3 run.py full "your search query"
```
