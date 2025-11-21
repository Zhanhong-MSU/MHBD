# TF-IDF Algorithm Implementation

## Overview

This project implements the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm for document analysis and retrieval. Two versions are provided:

1. **Single-threaded version** (`run_analysis.py`) - Simple, educational implementation
2. **Multi-process parallel version** (`run_analysis_parallel.py`) - Production-optimized with automatic CPU adaptation

Both use only Python standard library (no external dependencies required).

## Features

### ✅ Core Features (Both Versions)
- Complete TF-IDF algorithm implementation
- Document tokenization and preprocessing
- Multiple test queries across different topics
- Detailed results with relevance scoring
- Works with Python 3.6+

### ⚡ Parallel Version Additional Features
- **Automatic CPU core detection** - Adapts to your system
- **3-5x faster** on multi-core systems
- **Manual core override** - Control resource usage
- **Progress tracking** - Real-time execution status
- **Zero configuration** - Just run and it optimizes itself

## Requirements

- **Python**: 3.6 or higher
- **Operating System**: Any (Linux, macOS, Windows)  
- **Dependencies**: None (uses Python standard library only)

## Parallel Processing Technology

### How It Works

The parallel version (`run_analysis_parallel.py`) uses Python's `multiprocessing` module to distribute work across multiple CPU cores:

**1. Automatic CPU Detection**
```python
from multiprocessing import cpu_count
cores = cpu_count()  # Automatically detects available cores
```

**2. Parallel Workload Distribution**
- **Step 1**: Tokenize documents in parallel (each core processes ~N/k documents)
- **Step 2**: Calculate IDF sequentially (requires global word statistics)
- **Step 3**: Calculate TF-IDF scores in parallel (independent per document)

**3. Performance Optimization**
- Uses `multiprocessing.Pool` for efficient process management
- Automatic load balancing across CPU cores
- Minimal inter-process communication overhead

### Why Multiprocessing (Not Threading)?

Python's **Global Interpreter Lock (GIL)** prevents true parallel execution with threads for CPU-intensive tasks. Multiprocessing bypasses the GIL:

| Approach | CPU-bound Tasks | GIL Impact | Speedup |
|----------|----------------|------------|---------|
| Threading | ❌ No speedup | Limited by GIL | ~1.0x |
| Multiprocessing | ✅ True parallelism | No GIL limit | ~3-5x |

### Expected Performance

Based on Amdahl's Law (70% parallelizable code):

```
Speedup = 1 / (0.3 + 0.7/cores)

1 core:  1.0x (baseline)
2 cores: 1.8-2.0x
4 cores: 3.0-3.5x
8 cores: 5.0-6.0x
```

Actual performance may vary based on:
- CPU architecture and speed
- Available memory
- I/O performance
- System load

### Technical Details

For in-depth implementation details, see [`docs/PARALLEL_IMPLEMENTATION.md`](docs/PARALLEL_IMPLEMENTATION.md), which covers:
- Detailed parallel algorithm design
- Process pool pattern implementation
- Memory and overhead considerations
- Performance benchmarking methodology

## How to Run

### Option 1: Single-threaded Version (Simpler, Educational)

**Sample Dataset (10 documents)**
```bash
python3 run_analysis.py
```
- Execution time: < 1 second
- Best for: Learning, debugging, small datasets

**Full Dataset (17,901 documents)**
```bash
python3 run_analysis.py full
```
- Execution time: ~30-60 seconds
- Single-core processing

### Option 2: Multi-process Parallel Version (⚡ Recommended for Large Datasets)

**Sample Dataset with auto-detected CPU cores**
```bash
python3 run_analysis_parallel.py
```
- Execution time: < 1 second
- Automatically uses all available CPU cores

**Full Dataset with auto-detected CPU cores**
```bash
python3 run_analysis_parallel.py full
```
- Execution time: ~10-20 seconds (3-5x faster!)
- Adapts to your system's CPU configuration

**Specify CPU cores manually**
```bash
python3 run_analysis_parallel.py full 4    # Use exactly 4 cores
python3 run_analysis_parallel.py full 8    # Use exactly 8 cores
python3 run_analysis_parallel.py full 1    # Single-core mode
```

### Performance Comparison

| Dataset | Single-threaded | Parallel (2 cores) | Parallel (4 cores) | Parallel (8 cores) |
|---------|----------------|-------------------|-------------------|-------------------|
| Sample (10 docs) | < 1s | < 1s | < 1s | < 1s |
| Full (17,901 docs) | ~60s | ~30s (2x) | ~15s (4x) | ~10s (6x) |

**Note**: Actual speedup depends on your CPU. Use `python3 scripts/demo_cpu_detection.py` to see expected performance on your system.

### Check Your System's CPU Configuration

```bash
python3 scripts/demo_cpu_detection.py
```

This will display:
- Number of CPU cores available
- Expected speedup with parallel processing
- Recommended command for your system

### Benchmark Performance

Compare single-threaded vs parallel on your system:
```bash
python3 tests/benchmark_parallel.py full
```

This runs both versions and shows detailed performance comparison.

## Project Structure

```
tfidf/
├── run_analysis.py              # Main program - single-threaded version
├── run_analysis_parallel.py     # Main program - multi-process parallel version (faster)
├── README.md                    # This file
├── requirements.txt             # No dependencies (standard library only)
│
├── dataset/                     # Dataset folder
│   ├── newsgroups_sample/       # 10 sample documents (required)
│   └── newsgroups_full/         # 17,901 documents (optional)
│
├── scripts/                     # Utility scripts (optional)
│   ├── README.md
│   ├── download_full_newsgroups.py  # Download full dataset
│   └── demo_cpu_detection.py        # Check system CPU configuration
│
├── tests/                       # Test and benchmark files (optional)
│   ├── README.md
│   ├── benchmark_parallel.py    # Performance comparison tool
│   ├── test_both_datasets.py
│   └── test_optimized.py
│
└── docs/                        # Technical documentation (optional)
    ├── README.md
    └── PARALLEL_IMPLEMENTATION.md   # Detailed parallel implementation guide
```

### For Assignment Submission

**Core files (required)**:
```
tfidf/
├── run_analysis.py              # Choose ONE version:
OR  run_analysis_parallel.py     # - Simple (single-threaded) OR Optimized (parallel)
├── dataset/newsgroups_sample/   # 10 sample documents
└── README.md                    # This instructions file
```

**Optional files** (for reference):
- `scripts/` - Development utilities (dataset download, CPU detection)
- `tests/` - Performance testing and benchmarking tools
- `docs/` - Technical implementation documentation
- `dataset/newsgroups_full/` - Full dataset (may be too large for submission)

## Author

Student Assignment - November 2025
