# Test Files

This folder contains testing and benchmarking scripts for the TF-IDF implementation.

## Files

- **`test_both_datasets.py`** - Compares performance between sample (10 docs) and full (17,901 docs) datasets
- **`test_optimized.py`** - Tests optimized TF-IDF implementation with caching for large datasets

## Usage

These are development/testing files and are **not required** for the main assignment submission.

### Test Both Datasets

```bash
cd tests
python3 test_both_datasets.py
```

### Test Optimized Version

```bash
cd tests
python3 test_optimized.py
```

**Note**: These tests are for performance analysis and are not part of the core assignment.
