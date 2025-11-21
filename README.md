# TF-IDF Algorithm Assignment

## Overview

This project implements the **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm for document analysis and information retrieval. The implementation uses only Python standard library without any external dependencies.

## 📋 What to Submit

Submit the entire **`tfidf`** folder to your instructor. This folder contains:

```
tfidf/
├── run_analysis.py              # Main program (English comments)
├── documents/
│   ├── newsgroups_sample/       # 10 sample documents (required)
│   └── newsgroups_full/         # 17,901 documents (optional)
├── requirements.txt             # Empty (no dependencies needed)
└── README.md                    # Instructions
```

## 🚀 How to Run

### Quick Start - Single-threaded Version

**Sample Dataset (10 documents)**
```bash
cd tfidf
python3 run_analysis.py
```
**Execution time**: < 1 second  
**Dataset**: 10 documents from newsgroups

**Full Dataset (17,901 documents)**
```bash
python3 run_analysis.py full
```
**Execution time**: ~30-60 seconds  
**Dataset**: 17,901 documents from 20 Newsgroups

### Quick Start - Multi-process Parallel Version (⚡ Faster!)

**Sample Dataset with auto-detected CPU cores**
```bash
cd tfidf
python3 run_analysis_parallel.py
```
**Execution time**: < 1 second

**Full Dataset with auto-detected CPU cores**
```bash
python3 run_analysis_parallel.py full
```
**Execution time**: ~10-20 seconds (3-5x faster!)  
**Features**: 
- Automatically detects and uses all CPU cores
- Parallel document processing
- Real-time progress tracking

**Specify CPU cores manually**
```bash
python3 run_analysis_parallel.py full 4    # Use 4 cores
python3 run_analysis_parallel.py full 8    # Use 8 cores
```

### Performance Benchmark

Compare single-threaded vs parallel performance:
```bash
cd tfidf
python3 tests/benchmark_parallel.py full
```

### View Help

```bash
python3 run_analysis.py --help
python3 run_analysis_parallel.py --help
```

## 💡 For Instructors

To run this assignment after extraction:

1. Extract the `tfidf` folder
2. Open terminal and navigate to the folder:
   ```bash
   cd path/to/tfidf
   ```
3. Run the program:
   ```bash
   python3 run_analysis.py
   ```

**Requirements**:
- Python 3.6 or higher
- No external packages needed (uses standard library only)
- Works on Windows, macOS, and Linux

## 📊 What the Program Does

The program demonstrates TF-IDF algorithm by:

1. Loading documents from the dataset
2. Calculating Term Frequency (TF) for each document
3. Calculating Inverse Document Frequency (IDF) across all documents
4. Computing TF-IDF scores for 8 test queries
5. Ranking documents by relevance to each query
6. Displaying detailed analysis results with statistics

### Test Queries

1. "computer graphics image display"
2. "medical doctor patient health"
3. "politics government election"
4. "baseball game sport team"
5. "religion atheism god belief"
6. "science research study"
7. "software program algorithm"
8. "treatment disease clinical"

## 📁 Project Structure

```
MHBG-1/                              # Project root
├── README.md                        # This file (project overview)
├── homework_1.pdf                  # Original assignment (optional)
└── tfidf/                          # ⭐ SUBMIT THIS FOLDER
    ├── run_analysis.py             # Main TF-IDF program (single-threaded)
    ├── run_analysis_parallel.py    # Main TF-IDF program (multi-process, faster)
    ├── README.md                   # Usage instructions
    ├── requirements.txt            # No dependencies (standard library only)
    ├── documents/                  # Dataset folder
    │   ├── newsgroups_sample/      # 10 sample docs (required)
    │   └── newsgroups_full/        # 17,901 docs (optional)
    ├── scripts/                    # Utility scripts (optional)
    │   ├── README.md
    │   └── download_full_newsgroups.py
    └── tests/                      # Test files (optional)
        ├── README.md
        ├── benchmark_parallel.py   # Performance comparison tool
        ├── test_both_datasets.py
        └── test_optimized.py
```

### What to Submit

**Core files (required)**:
- `tfidf/run_analysis.py` - Single-threaded version (simpler)
- OR `tfidf/run_analysis_parallel.py` - Parallel version (demonstrates optimization)
- `tfidf/documents/newsgroups_sample/` - 10 sample documents
- `tfidf/README.md` - Instructions

**Optional files** (for reference):
- `tfidf/scripts/` - Dataset download tools
- `tfidf/tests/` - Performance testing and benchmark scripts
- `tfidf/documents/newsgroups_full/` - Full 17,901 documents
    ├── scripts/                    # Utility scripts (optional)
    │   ├── README.md
    │   └── download_full_newsgroups.py
    └── tests/                      # Test files (optional)
        ├── README.md
        ├── test_both_datasets.py
        └── test_optimized.py
```

### What to Submit

**Core files (required)**:
- `tfidf/run_analysis.py` - Main program
- `tfidf/documents/newsgroups_sample/` - 10 sample documents
- `tfidf/README.md` - Instructions

**Optional files** (for reference, not required):
- `tfidf/scripts/` - Dataset download tools
- `tfidf/tests/` - Performance testing scripts
- `tfidf/documents/newsgroups_full/` - Full 17,901 documents

## 🎯 Algorithm Implementation

### TF-IDF Formula

**Term Frequency (TF)**:
```
TF(term, document) = (Number of times term appears) / (Total terms in document)
```

**Inverse Document Frequency (IDF)**:
```
IDF(term) = log(Total documents / Documents containing term)
```

**TF-IDF Score**:
```
TF-IDF = TF × IDF
```

### Core Functions

- `clean_text()` - Tokenizes text into lowercase words
- `calculate_tf()` - Computes term frequency for each word
- `calculate_idf()` - Computes inverse document frequency
- `search_documents()` - Ranks documents by TF-IDF relevance
- `run_tfidf_analysis()` - Main analysis orchestration

## 🔧 Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (standard library only)
- **Code Style**: All comments in English
- **Dataset**: 20 Newsgroups (classic ML dataset)
- **Performance**: 
  - Sample: <1 second for 10 documents
  - Full: ~30-60 seconds for 17,901 documents

## 📖 Documentation

Detailed documentation is available in:
- `/tfidf/README.md` - Complete usage guide
- Inline code comments - Algorithm explanation

## 👤 Author

Student Assignment Submission  
Date: November 2025

---

**Note**: This is an academic assignment. The implementation focuses on clarity and educational value while maintaining professional code quality.
