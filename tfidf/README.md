# TF-IDF Algorithm Implementation

## Overview

This project implements the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm for document analysis and retrieval. The implementation uses only Python standard library (no external dependencies required).

## Requirements

- **Python**: 3.6 or higher
- **Operating System**: Any (Linux, macOS, Windows)  
- **Dependencies**: None (uses Python standard library only)

## How to Run

### Run on Sample Dataset (10 documents)

```bash
python3 run_analysis.py
```

**Execution time**: < 1 second

### Run on Full Dataset (17,901 documents)

```bash
python3 run_analysis.py full
```

**Execution time**: ~30-60 seconds

## Project Structure

```
tfidf/
├── run_analysis.py              # Main program
├── documents/
│   ├── newsgroups_sample/       # Sample dataset (10 documents)
│   └── newsgroups_full/         # Full dataset (17,901 documents)
└── README.md                    # This file
```

## Author

Student Assignment - November 2025
