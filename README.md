# TF-IDF Algorithm Assignment

## Overview

This project implements the **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm for document analysis and information retrieval. Two versions are provided:

1. **Single-threaded version** (`run_analysis.py`) - Simple, educational implementation
2. **Multi-process parallel version** (`run_analysis_parallel.py`) - Production-optimized with automatic CPU adaptation

Both use only Python standard library (no external dependencies required).

## 📋 What to Submit

Submit the entire **`tfidf`** folder to your instructor. This folder contains:

```
tfidf/
├── run_analysis.py              # Single-threaded version (simpler)
├── run_analysis_parallel.py     # Parallel version (faster, optimized)
├── dataset/
│   ├── newsgroups_sample/       # 10 sample documents (required)
│   └── newsgroups_full/         # 17,901 documents (optional)
├── requirements.txt             # Empty (no dependencies needed)
├── scripts/                     # CPU detection and utilities
├── tests/                       # Performance benchmarks
└── docs/                        # Technical documentation
```

## 🚀 Quick Start

### Single-threaded Version (Educational)

**Sample Dataset (10 documents)**
```bash
cd tfidf
python3 run_analysis.py
```
**Execution time**: < 1 second

**Full Dataset (17,901 documents)**
*Note: You must download the dataset first.*
```bash
python3 manage_dataset.py download
python3 run_analysis.py full
```
**Execution time**: ~30-60 seconds

### Multi-process Parallel Version (⚡ Recommended)

**Sample Dataset with auto-detected CPU cores**
```bash
cd tfidf
python3 run_analysis_parallel.py
```
**Execution time**: < 1 second

**Full Dataset with auto-detected CPU cores**
*Note: You must download the dataset first.*
```bash
python3 manage_dataset.py download
python3 run_analysis_parallel.py full
```
**Execution time**: ~10-20 seconds (3-5x faster!)

**With custom CPU cores and data sampling**
```bash
# Use 8 cores with full dataset
python3 run_analysis_parallel.py full 8

# Use 8 cores with half the data (for 8GB RAM systems)
python3 run_analysis_parallel.py full 8 0.5

# Use 8 cores with 1/8 data (quick test)
python3 run_analysis_parallel.py full 8 0.125
```

### Performance Benchmark

Compare single-threaded vs parallel:
```bash
python3 tests/benchmark_parallel.py full
```

### Check Your CPU Configuration

```bash
python3 scripts/demo_cpu_detection.py
```

## 📦 Managing the Full Dataset

To reduce project size for submission or email, you can delete the full dataset and restore it later using the provided script.

**Delete Full Dataset (to save space)**
```bash
cd tfidf
python3 manage_dataset.py delete
```

**Download & Restore Full Dataset**
```bash
cd tfidf
python3 manage_dataset.py download
```
*Note: This downloads the original 20 Newsgroups dataset (~14MB compressed) and reconstructs the file structure.*

## ✨ Features

### Core Features (Both Versions)
- ✅ Complete TF-IDF algorithm implementation
- ✅ Document tokenization and preprocessing
- ✅ Multiple test queries across different topics
- ✅ Detailed results with relevance scoring
- ✅ Works with Python 3.6+
- ✅ Zero external dependencies

### Parallel Version Additional Features
- ⚡ **Automatic CPU core detection** - Adapts to your system
- ⚡ **3-5x faster** on multi-core systems
- ⚡ **Dynamic chunk size optimization** - Better load balancing
- ⚡ **Data sampling support** - Process 1/2, 1/4, or 1/8 of data
- ⚡ **Progress tracking** - Real-time execution status
- ⚡ **Zero configuration** - Just run and it optimizes itself

## 📊 Performance Comparison

### Speed Comparison by Dataset Size

| Dataset | Single-threaded | Parallel (2 cores) | Parallel (4 cores) | Parallel (8 cores) |
|---------|----------------|-------------------|-------------------|-------------------|
| Sample (10 docs) | < 1s | < 1s | < 1s | < 1s |
| Full (17,901 docs) | ~60s | ~30s (2.0x) | ~15s (4.0x) | ~10s (6.0x) |

### Memory Usage with Data Sampling (8C8G System)

| Sampling | Documents | Memory | Time | Use Case |
|----------|-----------|--------|------|----------|
| 100% (full) | 17,901 | ~6-7GB | ~15s | Complete analysis |
| 50% | ~8,950 | ~3-4GB | ~8s | Quick testing |
| 25% | ~4,475 | ~2GB | ~4s | Development |
| 12.5% | ~2,237 | ~1GB | ~2s | Fast validation |

## ⚙️ Parallel Processing Technology

### How It Works

The parallel version uses Python's `multiprocessing` module to distribute work across CPU cores:

**1. Automatic CPU Detection**
```python
from multiprocessing import cpu_count
cores = cpu_count()  # Auto-detects available cores
```

**2. Three-Stage Parallel Pipeline**
- **Stage 1**: Tokenize documents in parallel (90% parallelizable)
- **Stage 2**: Calculate IDF sequentially (requires all docs)
- **Stage 3**: Score documents in parallel (90% parallelizable)

**3. Dynamic Load Balancing**
```python
# Optimize chunk size based on CPU cores
chunksize = max(1, num_docs // (num_cores * 4))
pool.map(process_document, docs, chunksize=chunksize)
```

### Why Multiprocessing (Not Threading)?

Python's **Global Interpreter Lock (GIL)** prevents true parallel execution with threads for CPU-intensive tasks:

| Approach | CPU-bound Tasks | GIL Impact | Speedup |
|----------|----------------|------------|---------|
| Threading | ❌ No speedup | Limited by GIL | ~1.0x |
| Multiprocessing | ✅ True parallelism | Bypasses GIL | ~3-5x |

### Expected Performance (Amdahl's Law)

With 90% parallelizable code:

```
Speedup = 1 / (0.1 + 0.9/cores)

2 cores:  1.82x
4 cores:  3.08x
8 cores:  5.26x
16 cores: 8.42x
```

**Note**: Actual speedup depends on CPU architecture, memory bandwidth, and I/O performance.

## 🎯 Algorithm Implementation

### TF-IDF Formula

**Term Frequency (TF)**:
```
TF(term, doc) = count(term in doc) / total_terms(doc)
```

**Inverse Document Frequency (IDF)**:
```
IDF(term) = log(total_docs / docs_containing(term))
```

**TF-IDF Score**:
```
TF-IDF(term, doc) = TF(term, doc) × IDF(term)
```

### Core Functions

- `clean_text()` - Tokenizes text into lowercase words
- `calculate_tf()` - Computes term frequency for each word
- `calculate_idf()` - Computes inverse document frequency
- `search_documents()` - Ranks documents by TF-IDF relevance
- `run_tfidf_analysis()` - Main analysis orchestration

### Test Queries

The program tests 8 queries across different topics:

1. "computer graphics image display"
2. "medical doctor patient health"
3. "politics government election"
4. "baseball game sport team"
5. "religion atheism god belief"
6. "science research study"
7. "software program algorithm"
8. "treatment disease clinical"

## 📁 Full Project Structure

```
MHBG-1/                              # Project root
├── README.md                        # ⭐ This file (complete guide)
├── homework_1.pdf                   # Original assignment
└── tfidf/                           # ⭐ SUBMIT THIS FOLDER
    ├── run_analysis.py              # Single-threaded version
    ├── run_analysis_parallel.py     # Multi-process parallel version
    ├── requirements.txt             # Empty (standard library only)
    │
    ├── dataset/                     # Dataset folder
    │   ├── newsgroups_sample/       # 10 sample docs (required)
    │   └── newsgroups_full/         # 17,901 docs (optional)
    │
    ├── scripts/                     # Utility scripts
    │   ├── README.md
    │   ├── demo_cpu_detection.py    # Check CPU configuration
    │   ├── test_cpu_utilization.py  # Test parallel efficiency
    │   └── download_full_newsgroups.py
    │
    ├── tests/                       # Performance tests
    │   ├── README.md
    │   ├── benchmark_parallel.py    # Speed comparison tool
    │   ├── test_both_datasets.py
    │   └── test_optimized.py
    │
    └── docs/                        # Technical documentation
        ├── README.md
        ├── PARALLEL_IMPLEMENTATION.md  # Parallel algorithm details
        └── CPU_OPTIMIZATION.md         # Multi-core optimization guide
```

### What to Submit

**Core files (required)**:
- `tfidf/run_analysis.py` OR `run_analysis_parallel.py` (choose one or both)
- `tfidf/dataset/newsgroups_sample/` - 10 sample documents
- `tfidf/README.md` - Instructions

**Optional files** (for reference):
- `tfidf/scripts/` - Development utilities
- `tfidf/tests/` - Performance benchmarks
- `tfidf/docs/` - Technical documentation
- `tfidf/dataset/newsgroups_full/` - Full dataset (may be large)

## 🔧 Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (standard library only)
- **Code Style**: All comments in English
- **Dataset**: 20 Newsgroups (classic ML dataset)
- **Parallel Technology**: multiprocessing.Pool
- **CPU Optimization**: Dynamic chunk size calculation

## 💡 For Instructors

To run this assignment after extraction:

1. Extract the `tfidf` folder
2. Open terminal and navigate:
   ```bash
   cd path/to/tfidf
   ```
3. Run either version:
   ```bash
   python3 run_analysis.py              # Simple version
   python3 run_analysis_parallel.py     # Optimized version
   ```

**System Requirements**:
- Python 3.6 or higher
- No external packages needed
- Works on Windows, macOS, and Linux
- Parallel version benefits from multi-core CPU

## 📖 Additional Documentation

- [`tfidf/docs/PARALLEL_IMPLEMENTATION.md`](tfidf/docs/PARALLEL_IMPLEMENTATION.md) - Detailed parallel algorithm
- [`tfidf/docs/CPU_OPTIMIZATION.md`](tfidf/docs/CPU_OPTIMIZATION.md) - Multi-core optimization guide
- [`tfidf/scripts/README.md`](tfidf/scripts/README.md) - Utility scripts documentation
- [`tfidf/tests/README.md`](tfidf/tests/README.md) - Testing and benchmarking guide

---

**Note**: This is an academic assignment demonstrating both educational clarity (single-threaded) and production optimization (parallel processing) approaches.
